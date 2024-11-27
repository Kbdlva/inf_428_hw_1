from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import csv

def bulk_insert_to_elasticsearch(csv_file):
    es = Elasticsearch(
        "https://localhost:9200", 
        basic_auth=("kabdu", "0i2JKfrLtr_NDAN8_tS4"),  # Provide username and password here
        verify_certs=True  # If you're running Elasticsearch with SSL and have no valid cert, set this to False
    )
    
    documents = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doc = {
                "_op_type": "index",  # You can use 'index' to create or update documents
                "_index": "your_index_name",  # Set your target index here
                "_source": {
                    "test": row['Test'],
                    "generated_data": row['Generated Data']
                }
            }
            documents.append(doc)
    
    # Insert the documents using the bulk helper function
    bulk(es, documents)

csv_file = "generated_data.csv"  # Path to your CSV file
bulk_insert_to_elasticsearch(csv_file)
