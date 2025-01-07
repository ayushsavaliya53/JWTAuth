pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/ayushsavaliya53/JWTAuth.git'
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-token') {
                        sh 'docker build -t my-django-app .'
                        sh 'docker tag my-django-app ayushsavaliya53/my-django-app:latest'
                        sh 'docker push ayushsavaliya53/my-django-app:latest'
                    }
                }
            }
        }
        stage('Deploy to Railway') {
            steps {
                withCredentials([string(credentialsId: 'railway-api-token', variable: 'RAILWAY_TOKEN')]) {
                    sh '''
                    curl -X POST "https://railway.app/api/deploy" \
                        -H "Authorization: Bearer ${RAILWAY_TOKEN}" \
                        -d '{"project_id": "e36b7193-669d-4831-9e2e-b8b979e05636"}'
                    '''
                }
            }
        }
    }
}
