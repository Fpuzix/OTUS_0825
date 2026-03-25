pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Клонирование репозитория...'
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo 'Установка зависимостей...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Запуск тестов...'
                sh '''
                    . venv/bin/activate
                     python3 -m pytest test_web_5/test_web_5.py --browser chrome --headless
                        --junitxml=reports/junit.xml \
                        --html=reports/report.html \
                        --cov=src \
                        --cov-report=xml:reports/coverage.xml \
                        --cov-report=html:reports/htmlcov
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Проверка качества кода...'
                sh '''
                    . venv/bin/activate
                    flake8 src/ tests/ --max-line-length=100 || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Публикация отчетов...'
            junit 'reports/junit.xml'
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        success {
            echo '✅ Сборка успешна!'
        }
        failure {
            echo '❌ Сборка провалена!'
        }
    }
}
