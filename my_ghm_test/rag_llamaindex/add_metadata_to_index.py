from llama_index.core import Document
from llama_index.core.schema import MetadataMode
from populate_metadata_sqlite import read_metadata_from_db

def add_metadata_to_index(documents):
    
    metadata_dict = read_metadata_from_db()
    
    for doc in documents:
        doc.metadata = {"metadata": {"title": "title", "author": "author", "date": "date"}}
        doc.metadata_mode = MetadataMode.METADATA_ONLY
