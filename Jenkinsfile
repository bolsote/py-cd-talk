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
        stage('static analysis') {
            steps {
                parallel (
                    "linting": {
                        sh '''
                            . ve/bin/activate
                            flake8 ./src || error=true
                            pylint ./src || error=true

                            if [ $error ]
                            then
                                exit 1
                            fi
                        '''
                    },
                    "types": {
                        sh '''
                            . ve/bin/activate
                            mypy ./src
                        '''
                    }
                )
            }
        }
        stage('unit tests') {
            steps {
                echo "You should run unit tests here"
            }
        }
        stage('security') {
            steps {
                sh '''
                    . ve/bin/activate
                    bandit -r src/
                    LC_ALL=en_GB.UTF-8 safety check
                '''
            }
        }
        stage('integration tests') {
            steps {
                echo "You should run integration tests here"
            }
        }
        stage('e2e tests') {
            steps {
                echo "You should run end to end tests here"
            }
        }
    }
}
