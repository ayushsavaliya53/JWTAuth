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
                withCredentials([
                    string(credentialsId: 'SECRET_KEY', variable: 'SECRET_KEY'),
                    string(credentialsId: 'EMAIL_HOST_PASSWORD', variable: 'EMAIL_HOST_PASSWORD'),
                    string(credentialsId: 'DATABASE_URL', variable: 'DATABASE_URL')
                ]) {
                    bat """
                        docker build ^
                            --build-arg SECRET_KEY="%SECRET_KEY%" ^
                            --build-arg EMAIL_HOST_PASSWORD="%EMAIL_HOST_PASSWORD%" ^
                            --build-arg DATABASE_URL="%DATABASE_URL%" ^
                            -t my-django-app .
                    """
                    bat "docker tag my-django-app ayushsavaliya53/my-django-app:latest"
                    bat "docker push ayushsavaliya53/my-django-app:latest"
                }
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
