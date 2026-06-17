#!/bin/bash

set -e

# Функция для сборки контейнеров
build() {
    echo "Сборка контейнеров..."
    docker compose -f lr-grafana/docker-compose.yml build
}

# Функция для старта контейнеров
start() {
    echo "Запуск контейнеров..."
    docker compose -f lr-grafana/docker-compose.yml up -d
}

# Функция для остановки контейнеров
stop() {
    echo "Остановка и удаление контейнеров..."
    docker compose -f lr-grafana/docker-compose.yml down --timeout 0
}

test() {
    docker compose -f lr-grafana/docker-compose.yml exec -it carbon-aggregator-test bash --rcfile /venv/bin/activate
}

# Обработка переданного аргумента
case "$1" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    test)
        test
        ;;
    *)
        echo "Использование: $0 {build|start|stop|test}"
        exit 1
        ;;
esac
