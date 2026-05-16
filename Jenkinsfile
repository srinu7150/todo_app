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
}
post {
    failure {
        script {
            def log = currentBuild.rawBuild.getLog(300).join('\n')

            def payload = groovy.json.JsonOutput.toJson([
                model: "qwen3.5-9b",
                messages: [[
                    role: "user",
                    content: "Summarize this Jenkins build failure in 5 bullets:\n${log}"
                ]],
                max_tokens: 400
            ])

            def response = httpRequest(
                url: 'http://192.168.1.6:1234/v1/chat/completions',
                httpMode: 'POST',
                contentType: 'APPLICATION_JSON',
                requestBody: payload,
                timeout: 60
            )

            def json = readJSON text: response.content
            def summary = json.choices[0].message.content

            slackSend message: "*Build Failed* — ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${summary}"
        }
    }
}