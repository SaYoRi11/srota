import os

from elasticsearch import Elasticsearch

def get_es():
	return Elasticsearch([{'host': '172.105.123.241', 'port': 9200}], http_auth=('elastic', 'elasticity00;;'))