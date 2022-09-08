pipeline {
    agent any

    stages {
        stage('build') {
            steps {
                sh 'make build'
            }
        }
        stage('test') {
            steps {
                sh 'make test'
            }
        }
        stage('lint') {
            steps {
                sh 'make lint'
            }
        }
        stage('setup') {
            steps {
                sh 'make setup'
            }
        }
        stage('docs') {
            steps {
                sh 'make docs'
            }
        }
        stage('html') {
            steps {
                sh 'make html'
                sh 'make clean'
            }
        }
    }
}
