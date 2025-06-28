pipeline {
    agent any

    environment {
        IMAGE_NAME = 'coref-app'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Docker Container') {
            steps {
                echo '🚀 Running Docker container...'
                sh 'docker run -d --rm -p 8501:8501 $IMAGE_NAME'
            }
        }
    }

    post {
        failure {
            echo '❌ Build failed. Check logs above.'
        }
        success {
            echo '✅ Build and container run successful.'
        }
    }
}
