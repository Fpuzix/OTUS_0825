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
                    pip install pytest-html pytest-cov flake8 || true
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Запуск тестов...'
                // Пишем команду в ОДНУ строку, чтобы аргументы точно не потерялись
                sh '''
                    . venv/bin/activate
                    python3 -m pytest test_web_5/test_web_5.py --browser chrome --headless --url "http://opencart:8080" --junitxml=junit.xml --html=report.html --alluredir=allure-results || true
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Проверка качества кода...'
                sh '''
                    . venv/bin/activate
                    flake8 . --exclude venv --max-line-length=100 || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Публикация отчетов...'
            // Публикуем JUnit (графики)
            junit 'junit.xml'

            // Публикуем HTML отчет
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Pytest HTML Report'
            ])

            // Если есть плагин Allure, раскомментируй:
            // allure includeProperties: false, results: [[path: 'allure-results']]
        }
        success {
            echo '✅ Сборка успешна!'
        }
        failure {
            echo '❌ Сборка провалена!'
        }
    }
}
