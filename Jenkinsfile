pipeline {
    agent any

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
                        "C:/Program Files/Git/bin/bash.exe" -c "docker build -t my-django-app ."
                        "C:/Program Files/Git/bin/bash.exe" -c "docker tag my-django-app ayushsavaliya53/my-django-app:latest"
                        "C:/Program Files/Git/bin/bash.exe" -c "docker push ayushsavaliya53/my-django-app:latest"
                    }
                }
            }
        }
        stage('Deploy to Railway') {
            steps {
                withCredentials([string(credentialsId: 'railway-api-token', variable: 'RAILWAY_TOKEN')]) {
                    "C:/Program Files/Git/bin/bash.exe" -c
                    '''
                    "curl -X POST "https://railway.app/api/deploy" \
                        -H "Authorization: Bearer ${RAILWAY_TOKEN}" \
                        -d '{"project_id": "e36b7193-669d-4831-9e2e-b8b979e05636"}'"
                    '''
                }
            }
        }
    }
}
