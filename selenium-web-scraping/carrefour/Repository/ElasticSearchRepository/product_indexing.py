import logging
from elasticsearch import Elasticsearch


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)


def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "members": {
                "dynamic": "strict",
                "products": {
                    "name": {
                        "type": "text"
                    },
                    "price_of": {
                        "type": "double"
                    },
                    "price_per": {
                        "type": "double"
                    },
                    "promotion": {
                        "type": "text"
                    },
                    "created": {
                        "type": "date",
                        "format": "dd-MM-yyyy HH:mm:ss"
                    },
                    "updated": {
                        "type": "date",
                        "format": "dd-MM-yyyy HH:mm:ss"
                    }
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(
                index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='products', body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
