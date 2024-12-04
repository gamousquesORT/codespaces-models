from enum import Enum
import sys, os
from llama_index.llms.azure_inference import AzureAICompletionsModel
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
import dotenv
import tiktoken
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler


token_counter = TokenCountingHandler(
    tokenizer=tiktoken.get_encoding("cl100k_base").encode
)
class ModelRole(Enum):
    QUERY = "Query"
    EMBED = "Embed"


class Model:
    llm_api_key = ""
    llm_api_url = ""
    model = ""
    llm = None
    temperature : float = 0.0
    def __init__(self, mode : ModelRole, model: str = "", temperature: float = 0.0):
        if not os.getenv("GITHUB_TOKEN"):
            raise ValueError("GITHUB_TOKEN is not set")
        
        if not isinstance(mode, ModelRole):
            raise ValueError(f"Invalid mode: {mode}. Expected one of: {[m.value for m in Mode]}")
        
        if model == "":
            raise ValueError("Model name is required")
        self.model = model

  
    def init_models(self):
        self.llm_api_key= os.environ["AZURE_INFERENCE_CREDENTIAL"] = os.getenv("GITHUB_TOKEN")
        self.llm_api_url= os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com/"
        self.llm = AzureAICompletionsModel(endpoint=self.llm_api_url, credential=self.llm_api_key, model_name=self.model,)                                           
        Settings.llm = self.llm
        Settings._callback_manager = CallbackManager([token_counter])
        
    def reset_token_counts(self):
        token_counter.reset_counts()
        
    def get_token_count(self) -> int:
        return token_counter.prompt_llm_token_count
        



class EmbedderModelOpenAI(Model):
    embed_model = None
    
    def __init__(self, model: str = ""):
        super().__init__(ModelRole.EMBED, model)             
        self.llm_api_key = os.environ["AZURE_INFERENCE_CREDENTIAL"] = os.getenv("GITHUB_TOKEN")
        self.llm_api_url= os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com/"
        self.model = model

    def init_models(self):
        self.embed_model = OpenAIEmbedding(
            api_key=self.llm_api_key,api_base=self.llm_api_url, model=self.model)
        Settings.embed_model = self.embed_model
        Settings._callback_manager = CallbackManager([token_counter])

    def get_token_count(self) -> int:
       return token_counter.embedding_token_counts
        

class EmbedderModelOpenAI(Model):
    embed_model = None
    
    def __init__(self, model: str = ""):
        super().__init__(ModelRole.EMBED, model)             
        self.llm_api_key = os.environ["AZURE_INFERENCE_CREDENTIAL"] = os.getenv("GITHUB_TOKEN")
        self.llm_api_url= os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com/"
        self.model = model

    def init_models(self):
        self.embed_model = OpenAIEmbedding(
            api_key=self.llm_api_key,api_base=self.llm_api_url, model=self.model)
        Settings.embed_model = self.embed_model
        Settings._callback_manager = CallbackManager([token_counter])
       
    def get_token_count(self) -> int:
        return token_counter.total_embedding_token_count
         
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

