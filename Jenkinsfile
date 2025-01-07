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
                        bash "docker build -t my-django-app ."
                        bash "docker tag my-django-app ayushsavaliya53/my-django-app:latest"
                        bash "docker push ayushsavaliya53/my-django-app:latest"
                    }
                }
            }
        }
        stage('Deploy to Railway') {
            steps {
                withCredentials([string(credentialsId: 'railway-api-token', variable: 'RAILWAY_TOKEN')]) {
                    bash
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
