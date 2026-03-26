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
                    python3 -m pytest test_web_5/test_web_5.py \
                        --browser chrome --headless --url "http://opencart:8080" \
                        --junitxml=junit.xml \
                        --html=report.html \
                        --alluredir=allure-results \
                        --cov=src \
                        --cov-report=xml:reports/coverage.xml \
                        --cov-report=html:reports/htmlcov || true
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Проверка качества кода...'
                sh '''
                    . venv/bin/activate
                    # Проверяем только те папки, которые реально существуют
                    flake8 . --exclude venv --max-line-length=100 || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Публикация отчетов...'
            junit 'junit.xml'

            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Pytest HTML Report'
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
