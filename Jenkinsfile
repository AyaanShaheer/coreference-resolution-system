pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/AyaanShaheer/coreference-resolution-system.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build('coref-system')
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    dockerImage.run('-p 8000:8000')
                }
            }
        }
    }
}
