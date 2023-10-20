import psycopg2
import json

with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

connection = psycopg2.connect(
    host=cfg['PostgreSQL']['host'],
    user=cfg['PostgreSQL']['user'],
    password=cfg['PostgreSQL']['password'],
    database=cfg['PostgreSQL']['database']
)

cursor = connection.cursor()
connection.autocommit = True