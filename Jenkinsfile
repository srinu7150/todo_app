pipeline {
    agent any

    options {
        skipDefaultCheckout true
        ansiColor('xterm')
    }

    environment {
        github_creds = credentials('guithub-creds')
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
}