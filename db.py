import os, sqlalchemy, urllib, databases

host_server = os.environ.get('HOST_SERVER')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('DB_SERVER_PORT')))
database_name = os.environ.get('DATABASE_NAME')
db_username = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_USER')))
db_password = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_PASSWORD')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('SSL_MODE')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)