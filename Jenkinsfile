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
    }
}
