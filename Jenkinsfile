pipeline {
    agent any

    environment {
        IMAGE_NAME = 'coref-app'
        CONTAINER_NAME = 'coref-container'
        PORT = '8000'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/AyaanShaheer/coreference-resolution-system.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    echo "Stopping existing container (if running)..."
                    sh '''
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                    '''

                    echo "Running Docker container..."
                    sh 'docker run -d -p $PORT:8000 --name $CONTAINER_NAME $IMAGE_NAME'
                }
            }
        }
    }
}
