import os

import bcrypt
from elasticsearch import Elasticsearch

def get_es():
	return Elasticsearch([{'host': '172.105.123.241', 'port': 9200}], http_auth=('elastic', 'elasticity00;;'))

def get_hashed_password(plain_text_password):
	pw = plain_text_password.encode('utf-8')
	return bcrypt.hashpw(pw, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    pw = plain_text_password.encode('utf-8')
    return bcrypt.checkpw(pw, hashed_password)