from enum import Enum
import sys, os
from llama_index.llms.azure_inference import AzureAICompletionsModel
from llama_index.core import Settings
import dotenv

class ModelRole(Enum):
    QUERY = "Query"
    EMBED = "Embed"

class Model:
    def __init__(self, mode : ModelRole, model: str = ""):
        if not os.getenv("GITHUB_TOKEN"):
            raise ValueError("GITHUB_TOKEN is not set")
        
        if not isinstance(mode, ModelRole):
            raise ValueError(f"Invalid mode: {mode}. Expected one of: {[m.value for m in Mode]}")
        
        if model == "":
            raise ValueError("Model name is required")
        

    @property
    def llm_api_key(self):
        return self.llm_api_key       
          
    @llm_api_key.setter
    def llm_api_key(self, value):
        self.llm_api_key = value
        
    @property
    def model(self):
        return self.model
    
    @model.setter
    def model(self, value):
        self.model = value
    
    
    def init_models(self):
        self.llm_api_key= os.environ["AZURE_INFERENCE_CREDENTIAL"] = os.getenv("GITHUB_TOKEN")
        self.llm_api_url= os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com/"
        self.llm = AzureAICompletionsModel(endpoint=self.llm_api_url, credential=self.llm_api_key, model_name=self.MODEL,)                                           
        Settings.llm = self.llm


class EmbedderModel(Model):
    def __init__(self, model: str = ""):
        super().__init__(ModelRole.EMBED, data_path, database_path, model)             
        super().llm_api_key = os.environ["AZURE_INFERENCE_CREDENTIAL"] = os.getenv("GITHUB_TOKEN")
        super().llm_api_url= os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com/"

    def init_models(self):
        self.embed_model = OpenAIEmbedding(
            model=self.EMBEDDER,
            api_key= super().llm_api_key,
            api_base= super().llm_api_url,
            )
        Settings.embed_model = self.embed_model

