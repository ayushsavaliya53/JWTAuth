pipeline {
    agent any

    environment {
        SECRET_KEY = credentials('SECRET_KEY')
        EMAIL_HOST_PASSWORD = credentials('EMAIL_HOST_PASSWORD')
        DATABASE_URL = credentials('DATABASE_URL')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/ayushsavaliya53/JWTAuth.git'
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-token') {
                        bat "docker build -t my-django-app ."
                        bat "docker tag my-django-app ayushsavaliya53/my-django-app:latest"
                        bat "docker push ayushsavaliya53/my-django-app:latest"
                    }
                }
            }
        }
        stage('Deploy to Railway') {
            steps {
                withCredentials([string(credentialsId: 'railway-api-token', variable: 'RAILWAY_TOKEN')]) {
                    bat '''
                    bash -c "curl -X POST 'https://railway.app/api/deploy' \
                        -H 'Authorization: Bearer ${RAILWAY_TOKEN}' \
                        -d '{\"project_id\": \"e36b7193-669d-4831-9e2e-b8b979e05636\"}'"
                    '''
                }
            }
        }
    }
}
