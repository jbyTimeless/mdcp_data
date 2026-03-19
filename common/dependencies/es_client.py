from elasticsearch import AsyncElasticsearch
from config.settings import settings

def get_es_client() -> AsyncElasticsearch:
    return AsyncElasticsearch([settings.es_host])

es_client = get_es_client()
