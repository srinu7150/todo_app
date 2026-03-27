"""
Flask Web Application for Todo Management
Self-contained with its own database models
"""
import os
from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin123.@localhost:5432/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set template folder to workspace root templates directory (absolute path)
import os
app.template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
app.static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
CORS(app)


# ============== Database Models (Self-contained) ==============

class User(db.Model, UserMixin):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    todos = db.relationship('Todo', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Todo(db.Model):
    """Todo item model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    user = db.relationship('User', back_populates='todos')
    
    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}')>"


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


# ============== Helper Functions ==============

def hash_password(password):
    """Hash a password for storing"""
    import bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """Verify a password against a hash"""
    import bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# ============== Routes ==============

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else to login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        if not username or len(username) < 3 or len(username) > 50:
            flash('Username must be between 3 and 50 characters.', 'danger')
            return render_template('register.html')
        
        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'danger')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use another email.', 'danger')
            return render_template('register.html')
        
        # Create new user
        try:
            new_user = User(
                username=username,
                email=email,
                password_hash=hash_password(password)
            )
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and verify_password(password, user.password_hash):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next', url_for('dashboard'))
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard showing user's todos"""
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.desc()).all()
    completed_count = Todo.query.filter_by(user_id=current_user.id, completed=True).count()
    pending_count = Todo.query.filter_by(user_id=current_user.id, completed=False).count()
    
    return render_template('dashboard.html', 
                         todos=todos,
                         completed_count=completed_count,
                         pending_count=pending_count)


@app.route('/todo/add', methods=['GET', 'POST'])
@login_required
def add_todo():
    """Add a new todo"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date_str = request.form.get('due_date', '')
        
        if not title:
            flash('Title is required.', 'danger')
            return render_template('add_todo.html')
        
        # Parse due date if provided (handles both date-only and datetime formats)
        due_date = None
        if due_date_str:
            try:
                # Try parsing ISO 8601 format with T separator (e.g., "2026-03-28T14:30" from datetime-local input)
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
            except ValueError:
                try:
                    # Try parsing with space separator (e.g., "2026-03-28 14:30")
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                except ValueError:
                    try:
                        # Try parsing date only (e.g., "2026-03-28" from calendar selection without time)
                        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                    except ValueError:
                        flash('Invalid date format. Use YYYY-MM-DD or select from calendar.', 'danger')
                        return render_template('add_todo.html')
        
        new_todo = Todo(
            user_id=current_user.id,
            title=title,
            description=description,
            due_date=due_date
        )
        db.session.add(new_todo)
        db.session.commit()
        
        flash('Todo added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_todo.html')


@app.route('/todo/<int:todo_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo(todo_id):
    """Edit an existing todo"""
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    
    if todo.user_id != current_user.id:
        flash('You can only edit your own todos.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        completed = request.form.get('completed') == 'on'
        due_date_str = request.form.get('due_date', '')
        
        if not title:
            flash('Title is required.', 'danger')
            return render_template('edit_todo.html', todo=todo)
        
        # Parse due date if provided (handles both date-only and datetime formats)
        due_date = todo.due_date
        if due_date_str:
            try:
                # Try parsing ISO 8601 format with T separator (e.g., "2026-03-28T14:30" from datetime-local input)
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
            except ValueError:
                try:
                    # Try parsing with space separator (e.g., "2026-03-28 14:30")
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                except ValueError:
                    try:
                        # Try parsing date only (e.g., "2026-03-28" from calendar selection without time)
                        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                    except ValueError:
                        flash('Invalid date format. Use YYYY-MM-DD or select from calendar.', 'danger')
                        return render_template('edit_todo.html', todo=todo)
        
        todo.title = title
        todo.description = description
        todo.completed = completed
        todo.due_date = due_date
        todo.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_todo.html', todo=todo)


@app.route('/todo/<int:todo_id>/toggle', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    
    if todo.user_id != current_user.id:
        flash('You can only toggle your own todos.', 'danger')
        return redirect(url_for('dashboard'))
    
    todo.completed = not todo.completed
    todo.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    
    flash(f'Todo marked as {"completed" if todo.completed else "pending"}!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/todo/<int:todo_id>/delete', methods=['POST'])
@login_required
def delete_todo(todo_id):
    """Delete a todo"""
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(todo)
    db.session.commit()
    
    flash('Todo deleted successfully.', 'info')
    return redirect(url_for('dashboard'))


@app.route('/stats')
@login_required
def stats():
    """Show statistics about todos"""
    total = Todo.query.filter_by(user_id=current_user.id).count()
    completed = Todo.query.filter_by(user_id=current_user.id, completed=True).count()
    pending = Todo.query.filter_by(user_id=current_user.id, completed=False).count()
    
    return render_template('stats.html',
                         total=total,
                         completed=completed,
                         pending=pending)


# ============== API Endpoints (for integration with FastAPI backend) ==============

@app.route('/api/todos', methods=['GET'])
@login_required
def api_get_todos():
    """Get all todos for current user"""
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'completed': t.completed,
        'due_date': t.due_date.isoformat() if t.due_date else None,
        'created_at': t.created_at.isoformat(),
        'updated_at': t.updated_at.isoformat()
    } for t in todos])


@app.route('/api/todos', methods=['POST'])
@login_required
def api_create_todo():
    """Create a new todo"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    new_todo = Todo(
        user_id=current_user.id,
        title=data['title'],
        description=data.get('description', ''),
        due_date=datetime.fromisoformat(data['due_date']).replace(tzinfo=timezone.utc) if data.get('due_date') else None
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify({
        'id': new_todo.id,
        'title': new_todo.title,
        'description': new_todo.description,
        'completed': new_todo.completed,
        'due_date': new_todo.due_date.isoformat() if new_todo.due_date else None
    }), 201


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@login_required
def api_update_todo(todo_id):
    """Update a todo"""
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if data.get('title'):
        todo.title = data['title']
    if data.get('description') is not None:
        todo.description = data['description']
    if data.get('completed') is not None:
        todo.completed = data['completed']
    if data.get('due_date'):
        todo.due_date = datetime.fromisoformat(data['due_date']).replace(tzinfo=timezone.utc)
    
    todo.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'due_date': todo.due_date.isoformat() if todo.due_date else None
    })


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def api_delete_todo(todo_id):
    """Delete a todo"""
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'message': 'Todo deleted successfully'}), 200


# ============== Error Handlers ==============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🎉 Flask Todo App Starting...")
    print("=" * 60)
    print("Access the application at: http://localhost:5000")
    print("Dashboard: http://localhost:5000/dashboard")
    print("API Docs: http://localhost:5000/api/todos")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
