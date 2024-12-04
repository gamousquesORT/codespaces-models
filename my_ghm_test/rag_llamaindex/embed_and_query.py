from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from enum import Enum
from llama_index.llms.azure_inference import AzureAICompletionsModel

import chromadb

import logging
import sys
from typing import List, Dict, Any
from pathlib import Path
from model import Model
from exec_test_source_files.populate_metadata_sqlite import read_metadata_from_db

class OperationMode(Enum):
    INGEST = "ingest"
    RETRIEVE = "retrieve"
    CLEANUP = "cleanup"
    
    
class RagBasedBot:
    query_model = None
    embedding_model = None
    db_client = None
    path_to_documents = None
    metadata_dict = None
    
    def __init__(self, mode : OperationMode, data_path: str, database_path:str, model_for_query:Model = None, model_for_embedding:Model = None):
        self.query_model = model_for_query
        self.embedding_model = model_for_embedding
        
        try:
            if not isinstance(mode, OperationMode):
                raise ValueError(f"Invalid mode: {mode}. Expected one of: {[m.value for m in OperationMode]}")
            
            self.path_to_documents = data_path
            self.db_path = database_path
            
            if self.query_model != None and mode == OperationMode.RETRIEVE:
                self.query_model.init_models()
            
            if self.embedding_model == None:
                raise ValueError("Embedding model is required")
            else:  
                self.embedding_model.init_models()
        
            if mode == OperationMode.INGEST:
                self._init_vector_store()
            elif mode == OperationMode.RETRIEVE:
                self._load_vector_store()
            elif mode == OperationMode.CLEANUP:
                self._delete_embeddings()
        except ValueError as e:
            logging.error(e)
            sys.exit(1)
        except Exception as e:  
            logging.error(e)
            sys.exit(1)
            
        
    def _init_vector_store(self):
        self.db_client = chromadb.PersistentClient(path=self.db_path)
        self.chroma_collection = self.db_client.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # usar codigo de ejemplo de aca https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/ChromaIndexDemo.ipynb#scrollTo=9c3a56a5
    def _delete_embeddings(self):
        self.db_client = chromadb.PersistentClient(path=self.db_path)
        self.db_client.delete_collection("quickstart")

    def get_metadata_associated_to_element_name(self, search_key:str, search_name_value:str) -> Dict[str, Any]:
        element_name = Path(search_name_value).name
        for d in  self.metadata_dict:
            target_element = Path(d.get(search_key)).name
            if target_element == element_name:
                return d
        return None

    
    def index_data(self, rec_flag: bool = False):
        documents = SimpleDirectoryReader(self.path_to_documents, filename_as_id=True, recursive=rec_flag).load_data()
        
        self.metadata_dict = read_metadata_from_db()
        for doc in documents:
            item_metadata = self.get_metadata_associated_to_element_name('internal_source_URL', doc.metadata['file_name'])
            if item_metadata != None:
                doc.metadata.update(item_metadata)
                # excluir metadata 
                # filepath
                #  internal_source_URL
                # File_name
                doc.excluded_embed_metadata_keys.append('filepath')
                doc.excluded_embed_metadata_keys.append('internal_source_URL')
                doc.excluded_embed_metadata_keys.append('File_name')

        self.index = VectorStoreIndex.from_documents(documents, self.storage_context, insert_batch_size=250)
        self.index.storage_context.persist(persist_dir=self.db_path)
             
 
    def _load_vector_store(self):
        self.db_client = chromadb.PersistentClient(path=self.db_path)
        self.chroma_collection = self.db_client.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_vector_store(vector_store, storage=self.storage_context)            

    def _retrieve_embeddings_for_prompt(self, prompt: str):
        retriever = self.index.as_retriever()
        fragments = retriever.retrieve(prompt)
        return fragments
    
    def retrieve_answer(self, prompt: str):
        fragments = self._retrieve_embeddings_for_prompt(prompt)
        context = "\n------\n".join([ fragment.text for fragment in fragments ])

        messages = [
            ChatMessage(role="system", content='''Eres un asistente de IA especializado en responder preguntas sobre documentos, procedimientos, videos y otros recursos relacionados con el departamento de ingeniería de software de una universidad ORT Uruguay. Al responder a los usuarios:
                                                    - **Utiliza solo la información proporcionada en el apartado "Contexto" a continuación.**
                                                    - **Si tienes incertidumbre o necesitas más información para proporcionar una respuesta precisa, pide amablemente al usuario una aclaración.**
                                                    - **Si la respuesta no está en el contexto y no puedes obtener una aclaración, informa al usuario que la información no está disponible.**
                                                    - **Proporciona respuestas claras, concisas y precisas.**
                                                    - **Utiliza un lenguaje conciso y claro, adaptado a una audiencia de nivel universitario. **

                                                **Contexto:**''' + context),
            ChatMessage(role="user", content=prompt)
    
        ]

        self.query_model.llm
        response = Settings.llm.chat(messages)
        return response.__str__()



