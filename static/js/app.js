/**
 * Todo App - Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add confirmation for delete actions
    const deleteForms = document.querySelectorAll('[method="POST"]');
    deleteForms.forEach(function(form) {
        if (form.action.includes('/delete')) {
            form.addEventListener('submit', function(e) {
                if (!confirm('Are you sure you want to delete this todo?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Add smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add ripple effect to buttons (optional enhancement)
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'scale(0)';
            ripple.style.pointerEvents = 'none';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            
            requestAnimationFrame(function() {
                ripple.style.transition = 'transform 0.6s ease-out, opacity 0.6s ease-out';
                ripple.style.transform = 'scale(2.5)';
                ripple.style.opacity = '0';
                
                setTimeout(function() {
                    ripple.remove();
                }, 600);
            });
        });
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N: New todo
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            window.location.href = '{{ url_for("add_todo") }}';
        }
        
        // Escape: Close modals (if any)
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(function(modal) {
                const bootstrapModal = bootstrap.Modal.getInstance(modal);
                if (bootstrapModal) {
                    bootstrapModal.hide();
                }
            });
        }
    });

    // Add form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const invalidInputs = form.querySelectorAll('.is-invalid');
            if (invalidInputs.length > 0) {
                event.preventDefault();
                invalidInputs.forEach(function(input) {
                    input.focus();
                });
            }
        });
    });

    console.log('Todo App initialized successfully! 🎉');
});
