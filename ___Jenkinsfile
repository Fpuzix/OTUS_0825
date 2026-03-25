pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        PYTHONUNBUFFERED = '1'
        BASE_UI_URL = 'https://www.saucedemo.com/'
        BASE_API_URL = 'https://httpbin.org'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create venv') {
            steps {
                bat '''
                if not exist venv (
                    py -m venv venv
                )
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run API tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                pytest tests\\api -m api ^
                  --base-api-url=%BASE_API_URL% ^
                  --alluredir=allure-results
                '''
            }
        }

        stage('Run UI tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                pytest tests\\ui -m ui ^
                  --headless ^
                  --base-ui-url=%BASE_UI_URL% ^
                  --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**/*.*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'allure-results/**/*.*', allowEmptyArchive: true

            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }
    }
}


// pipeline {
//     agent any
//
//     options {
//         timestamps()
//         disableConcurrentBuilds()
//     }
//
//     environment {
//         PYTHONUNBUFFERED = '1'
//         BASE_UI_URL = 'https://www.saucedemo.com/'
//         BASE_API_URL = 'https://httpbin.org'
//     }
//
//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }
//
//         stage('Create venv') {
//             steps {
//                 bat '''
//                 if not exist venv (
//                     py -m venv venv
//                 )
//                 '''
//             }
//         }
//
//         stage('Install dependencies') {
//             steps {
//                 bat '''
//                 call venv\\Scripts\\activate
//                 python -m pip install --upgrade pip
//                 pip install -r requirements.txt
//                 '''
//             }
//         }
//
//         stage('Run API tests') {
//             steps {
//                 bat '''
//                 call venv\\Scripts\\activate
//                 pytest tests\\api -m api ^
//                   --base-api-url=%BASE_API_URL% ^
//                   --alluredir=allure-results
//                 '''
//             }
//             post {
//                 always {
//                     junit testResults: 'reports/api-junit.xml', allowEmptyResults: true
//                 }
//             }
//         }
//
//         stage('Run UI tests') {
//             steps {
//                 bat '''
//                 call venv\\Scripts\\activate
//                 pytest tests\\ui -m ui ^
//                   --headless ^
//                   --base-ui-url=%BASE_UI_URL% ^
//                   --alluredir=allure-results
//                 '''
//             }
//         }
//     }
//
//     post {
//         always {
//             archiveArtifacts artifacts: 'artifacts/**/*.*', allowEmptyArchive: true
//             archiveArtifacts artifacts: 'allure-results/**/*.*', allowEmptyArchive: true
//
//             allure([
//                 includeProperties: false,
//                 jdk: '',
//                 results: [[path: 'allure-results']]
//             ])
//         }
//     }
// }