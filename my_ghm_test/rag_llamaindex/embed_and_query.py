from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
from model_data import Model

import logging
import sys

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from enum import Enum
from llama_index.llms.azure_inference import AzureAICompletionsModel

class Mode(Enum):
    INGEST = "ingest"
    RETRIEVE = "retrieve"
    CLEANUP = "cleanup"
    
    
class RagBasedBot:
    query_model = None
    embedding_model = None
    db_client = None
    def __init__(self, mode : Mode, data_path: str, database_path:str, model_for_query:Model = None, model_for_embedding:Model = None):
        self.query_model = model_for_query
        self.embedding_model = model_for_embedding
        
        try:
            if not isinstance(mode, Mode):
                raise ValueError(f"Invalid mode: {mode}. Expected one of: {[m.value for m in Mode]}")
            
            self.path_to_documents = data_path
            self.db_path = database_path
            
            if self.query_model != None and mode == Mode.RETRIEVE:
                self.query_model.init_models()
            
            if self.embedding_model == None:
                raise ValueError("Embedding model is required")
            else:  
                self.embedding_model.init_models()
        
            if mode == Mode.INGEST:
                self._init_vector_store()
            elif mode == Mode.RETRIEVE:
                self._load_vector_store()
            elif mode == Mode.CLEANUP:
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

        
    def index_data(self, rec_flag: bool = False):
        documents = SimpleDirectoryReader(self.path_to_documents, recursive=rec_flag).load_data()
        self.index = VectorStoreIndex.from_documents(documents, self.storage_context, insert_batch_size=150)
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
            ChatMessage(role="system", content="Tú eres Tab el amable asistente de los docentes de la cátedra de ingeniería de software, la cual es parte de la facultad de ingeniería. Conoces los procedimientos y reglamentos de la facultad y de la cátedra, manejas información sobre materias, sobre la utilización de documentos del tipo, plantillas o templates y todo lo que los docentes necesitan para hacer su trabajo.  Trata de responder las preguntas con la mayor precisión posible. Si no sabes la respuesta, contesta que no tienes información para responder. Utiliza como contexto para elaborar la respuesta los siguientes datos: " + context),
            ChatMessage(role="user", content=prompt)
    
        ]

        self.query_model.llm
        response = Settings.llm.chat(messages)
        print("**\n\n")
        print(response)
        return response.__str__()



