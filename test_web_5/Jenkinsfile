pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: '', description: 'Версия (оставь пустой для последней)')
        string(name: 'APP_URL', defaultValue: 'http://opencart:8080/', description: 'URL Опенкарта')
        string(name: 'EXECUTOR_ADDR', defaultValue: 'http://selenoid:4444/wd/hub', description: 'Адрес Selenoid/GGR')
        choice(name: 'EXECUTOR_TYPE', choices: ['local', 'selenoid'], description: 'Где запускать?')
        string(name: 'THREADS', defaultValue: '1', description: 'Количество потоков')
    }

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
                    pip install pytest-html pytest-cov flake8 allure-pytest pytest-xdist || true
                '''
            }
        }

        stage('Test') {
            environment {
                SELENOID_URL = "${params.EXECUTOR_ADDR}"
            }
            steps {
                echo "Запуск тестов на ${params.BROWSER} для ${params.APP_URL}"
                sh """
                    . venv/bin/activate
                    python3 -m pytest test_web_5/test_web_5.py \
                        --browser ${params.BROWSER} \
                        --browser_version "${params.BROWSER_VERSION}" \
                        --executor ${params.EXECUTOR_TYPE} \
                        --url ${params.APP_URL} \
                        -n ${params.THREADS} \
                        --headless \
                        --junitxml=junit.xml \
                        --alluredir=allure-results || true
                """
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
            junit 'junit.xml'
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']],
                   commandline: 'allure'
        }
        success {
            echo 'Сборка успешна!'
        }
        failure {
            echo '!!!!!! Сборка провалена !!!!!!'
        }
    }
}
