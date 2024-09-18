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

class RagBasedBot:
    def __init__(self, data_path: str, database_path:str, model: str = "", embedder_model: str = ""):
        if not os.getenv("GITHUB_TOKEN"):
            raise ValueError("GITHUB_TOKEN is not set")

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
        self._init_vector_store()

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
        chroma_collection = self.db_client.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

        
    def index_data(self, rec_flag: bool = False):
        documents = SimpleDirectoryReader(self.path_to_documents, recursive=rec_flag).load_data()
        self.index = VectorStoreIndex.from_documents(documents, self.StorageContext, insert_batch_size=150)
             
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

def main():
    
    current_directory = os.path.dirname(__file__)
    data_path = os.path.join(current_directory, "./data")
    
    bot = RagBasedBot(data_path)
    bot.index_data()
    
    while True:
        prompt = input("/n/nQué pregunta tienes (o Enter para salir): ")
        if prompt == "":
            break
        response = bot.retrieve_answer(prompt)
        print(response)
        


if __name__ == "__main__":
    main()