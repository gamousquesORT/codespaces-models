from embed_and_query import RagBasedBot, Mode
from model_data import EmbedderModelOpenAI
import os

def main():
    
    current_directory = os.path.dirname(__file__)
    data_path = os.path.join(current_directory, "./data")
    data_base_path = os.path.join(current_directory, "./index_store")
    embedding_model = EmbedderModelOpenAI(model="text-embedding-3-large")
    RagBasedBot(mode=Mode.CLEANUP, data_path=data_path, database_path=data_base_path, model_for_embedding= embedding_model)


    

if __name__ == "__main__":
    main()