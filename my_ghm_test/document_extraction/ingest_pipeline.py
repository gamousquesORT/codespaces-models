from document_data_extracter import DocumentDataExtraction
import os

def main():
    GPT_MODEL = "gpt-4o-mini"

    file_name = 'example.txt'
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, file_name)

    path = os.path.abspath(__file__)
    read_path= path.joinpath("./data/hotel_invoices/receipts_2019_de_hotel")
    write_path= path.joinpath("./my_ghm_test/data/hotel_invoices/extracted_invoice_json")

    data_extractor = DocumentDataExtraction(read_path, write_path, GPT_MODEL)
    data_extractor.extract()


if __name__ == "__main__":
    main()