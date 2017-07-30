pipeline {
    agent any

    stages {
        stage('setup') {
            steps{
                sh '''
                    python3 -m venv ve
                    . ve/bin/activate
                    pip install -r test_requirements.txt
                '''
            }
        }
 
        stage('linting') {
            steps {
                sh '''
                    . ve/bin/activate
                    flake8 ./src
                    pylint ./src
                '''
            }
        }
    }
}
