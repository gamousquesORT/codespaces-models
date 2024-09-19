from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
import logging
import sys, os
import dotenv
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from enum import Enum

class Mode(Enum):
    INGEST = "ingest"
    RETRIEVE = "retrieve"
    
    
class RagBasedBot:
    def __init__(self, mode : Mode, data_path: str, database_path:str, model: str = "", embedder_model: str = ""):
        if not os.getenv("GITHUB_TOKEN"):
            raise ValueError("GITHUB_TOKEN is not set")
        
        if not isinstance(mode, Mode):
            raise ValueError(f"Invalid mode: {mode}. Expected one of: {[m.value for m in Mode]}")
        
        self.llm_api_key= os.environ["OPENAI_API_KEY"] = os.getenv("GITHUB_TOKEN")
        self.llm_api_url= os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com/"
            
        if  model == "":
            self.MODEL = "gpt-4o-mini"
            self.EMBEDDER = "text-embedding-3-large"
        else:
            self.MODEL = model
            self.EMBEDDER = embedder_model

        self.path_to_documents = data_path
        self.db_path = database_path

        self._init_models()
        
        if mode == Mode.INGEST:
            self._init_vector_store()
        elif mode == Mode.RETRIEVE:
            self._load_vector_store()


    def _init_models(self):
        self.llm = OpenAI(
            api_key=self.llm_api_key,
            api_base=self.llm_api_url,
            model=self.MODEL,
            )

        self.embed_model = OpenAIEmbedding(
            model=self.EMBEDDER,
            api_key=self.llm_api_key,
            api_base=self.llm_api_url,
            )
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        
    def _init_vector_store(self):
        self.db_client = chromadb.PersistentClient(path=self.db_path)
        self.chroma_collection = self.db_client.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # usar codigo de ejemplo de aca https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/ChromaIndexDemo.ipynb#scrollTo=9c3a56a5
    
    def index_data(self, rec_flag: bool = False):
        documents = SimpleDirectoryReader(self.path_to_documents, recursive=rec_flag).load_data()
        self.index = VectorStoreIndex.from_documents(documents, self.storage_context, insert_batch_size=150)
        self.index.storage_context.persist(persist_dir=self.index_store_path)
             
 
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
            ChatMessage(role="system", content="You are a helpful assistant that answers some questions with the help of some context data.\n\nHere is the context data:\n\n" + context),
            ChatMessage(role="user", content=prompt)
    
        ]

        response = self.llm.chat(messages)
        return response



