import os

from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    os.environ.get('DB_USER', 'pokedex'),
    user=os.environ.get('DB_USER', 'pokedex'),
    password=os.environ.get('DB_PASSWORD', 'pokedex'),
    host=os.environ.get('DB_HOST', 'localhost'),
    autorollback=True
)
