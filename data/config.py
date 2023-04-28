import logging
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_PORT = os.getenv('APP_PORT')

BASE_URL = os.getenv('BASE_URL')
WEBHOOK_PATH = f'/telegram'
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'


LOGGING_LEVEL = logging.DEBUG

ADMIN = os.getenv('ADMIN')

POSTGRES_CREDS = os.getenv('POSTGRES_CREDS')

REDIS_CREDS = {
    'host':     'localhost',
    'password': ''
}
