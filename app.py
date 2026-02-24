import asyncio
import os
import logging
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(os.getenv('APP_NAME', 'App'))

async def run():
    # Получаем конфигурацию из переменных окружения
    app_name = os.getenv('APP_NAME', 'UnknownApp')
    input_subject = os.getenv('INPUT_SUBJECT', 'app.input')
    output_subject = os.getenv('OUTPUT_SUBJECT', 'app.output')
    nats_servers = os.getenv('NATS_SERVERS', 'nats://nats-service:4222')

    logger.info(f"Starting {app_name}. Listening on '{input_subject}', publishing to '{output_subject}'")

    # Подключаемся к NATS
    nc = NATS()
    try:
        await nc.connect(servers=[nats_servers])
        logger.info(f"Connected to NATS at {nats_servers}")
    except Exception as e:
        logger.error(f"Failed to connect to NATS: {e}")
        return

    # Функция-обработчик входящих сообщений
    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        logger.info(f"[{app_name}] Received a message on '{subject}': {data}")

        # Логируем факт получения
        logger.info(f"Processing complete for {app_name}")

        # Отправляем дальше в следующий топик
        if output_subject:
            logger.info(f"[{app_name}] Forwarding message to '{output_subject}'")
            await nc.publish(output_subject, msg.data)
            logger.info(f"[{app_name}] Message forwarded")

    try:
        await nc.subscribe(input_subject, cb=message_handler)
        logger.info(f"Subscribed to '{input_subject}'")
    except Exception as e:
        logger.error(f"Failed to subscribe: {e}")

    # Держим соединение открытым
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    finally:
        loop.close()
