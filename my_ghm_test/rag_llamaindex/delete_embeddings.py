from embed_data import RagBasedBot, Mode

import os

def main():
    
    current_directory = os.path.dirname(__file__)
    data_path = os.path.join(current_directory, "./data")
    data_base_path = os.path.join(current_directory, "./index_store")
    
    bot = RagBasedBot(Mode.CLEANUP, data_path, data_base_path)

    

if __name__ == "__main__":
    main()