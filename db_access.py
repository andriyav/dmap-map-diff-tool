import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()
def db_access_stage():
    return psycopg2.connect(
        host=os.getenv('HOST_STAGE'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER_STAGE'),
        password=os.getenv('PASSWORD_STAGE')
    )

def db_access_prod():
    return psycopg2.connect(
        host=os.getenv('HOST_PROD'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER_PROD'),
        password=os.getenv('PASSWORD_PROD')
    )