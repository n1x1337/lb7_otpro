# Запуск проекта

**Очередь автоматическая очищается при перезапуске**

## Шаги для запуска

1. **Установите зависимости**  
   Установите необходимые зависимости для проекта:
   ```bash
   pip install -r requirements.txt

2. **Запустите RabbitMQ**
    Используйте Docker для запуска RabbitMQ:
    ```bash
    docker-compose up -d

3. **Запустите Producer**
    Передайте URL в качестве аргумента:
    ```bash
    python producer.py https://example.com

4. **Запустите Consumer**
    Для обработки сообщений из очереди:
    ```bash
    python consumer.py

