pipeline {
    agent any

    options {
        skipDefaultCheckout true
        ansiColor('xterm')
    }

    environment {
        github_creds = credentials('github-creds')
    }

    stages {
        stage('checkout') {
            steps {
                script {
                    deleteDir()
                    checkout scm
                }
            }
        }
    }
    post {
      failure {
        sh '''
          LOG=$(cat /tmp/build.log | tail -300)

          SUMMARY=$(curl -s http://your-llm-host:11434/v1/chat/completions \
            -H "Content-Type: application/json" \
            -d "{
              \"model\": \"llama3\",
              \"messages\": [{
                \"role\": \"user\",
                \"content\": \"Summarize this Jenkins error log in 5 bullets:\\n${LOG}\"
              }],
              \"max_tokens\": 400
            }" | jq -r '.choices[0].message.content')

          echo "$SUMMARY"
        '''
      }
    }
}