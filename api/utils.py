import os

import bcrypt
from elasticsearch import Elasticsearch

def get_es():
	return Elasticsearch([{'host': os.environ.get('ELASTIC_URI'), 'port': 9200}], http_auth=('elastic', os.environ.get('ELASTIC_PASSWORD')))

def get_hashed_password(plain_text_password):
	pw = plain_text_password.encode('utf-8')
	return bcrypt.hashpw(pw, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    pw = plain_text_password.encode('utf-8')
    return bcrypt.checkpw(pw, hashed_password)