import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = str(os.getenv("TELEGRAM_API_TOKEN"))

admin_id = [
   362763273
   #1063579292
]


ip = os.getenv('ip')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))
OAUTH_TOKEN = str(os.getenv('OAUTH_TOKEN'))
FOLDER_ID = str(os.getenv('FOLDER_ID'))

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'