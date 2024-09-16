from document_data_extracter import DocumentDataExtraction
import os

def main():
    GPT_MODEL = "gpt-4o-mini"

    current_directory = os.path.dirname(__file__)

    read_path= os.path.join(current_directory, "./dataEvents/source")
    write_path= os.path.join(current_directory, "./dataEvents/extracted")

    data_extractor = DocumentDataExtraction(read_path, write_path, GPT_MODEL)
    data_extractor.extract()


if __name__ == "__main__":
    main()