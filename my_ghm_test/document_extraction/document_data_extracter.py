from openai import OpenAI
import dotenv
import os
import io
from pillow import Image
import base64
import json


class DocumentDataExtraction:
    def __init__(self, read_files_path: str, out_data_path: str , model: str = ""):
        self._load_environs()
        
        if not model:
            self.MODEL = "gpt-4o-mini"
        else:
            self.MODEL = model

        self.path_to_documents = read_files_path
        self.path_to_output = out_data_path
        
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )



    @staticmethod
    def _load_environs():
        dotenv.load_dotenv()
        if not os.getenv("GITHUB_TOKEN"):
            raise ValueError("GITHUB_TOKEN is not set")
        os.environ["OPENAI_API_KEY"] = os.getenv("GITHUB_TOKEN")
        os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com/"


    @staticmethod
    def _encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


    def pdf_to_base64_images(self, pdf_path):
        #Handles PDFs with multiple pages
        pdf_document = fitz.open(pdf_path)
        base64_images = []
        temp_image_paths = []

        total_pages = len(pdf_document)

        for page_num in range(total_pages):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            temp_image_path = f"temp_page_{page_num}.png"
            img.save(temp_image_path, format="PNG")
            temp_image_paths.append(temp_image_path)
            base64_image = encode_image(temp_image_path)
            base64_images.append(base64_image)

        for temp_image_path in temp_image_paths:
            os.remove(temp_image_path)

        return base64_images
    
    def extract_from_multiple_pages(self, base64_images, original_filename, output_directory):
        entire_invoice = []

        for base64_image in base64_images:
            invoice_json = self.extract_invoice_data(base64_image)
            invoice_data = json.loads(invoice_json)
            entire_invoice.append(invoice_data)

        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Construct the output file path
        output_filename = os.path.join(output_directory, original_filename.replace('.pdf', '_extracted.json'))
        
        # Save the entire_invoice list as a JSON file
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(entire_invoice, f, ensure_ascii=False, indent=4)
        return output_filename

    def extract(self):
        # Print the current working directory
        current_directory = os.getcwd()
        print(f"The current working directory is: {current_directory}")
        
        # to save tokens we will only do the first 3 invoices
        for filename in os.listdir(self.path_to_documents)[:3]:
            file_path = os.path.join(self.path_to_documents, filename)
            print(f"Extracting data from {file_path}")
            if os.path.isfile(file_path):
                base64_images = self.pdf_to_base64_images(file_path)
                self.extract_from_multiple_pages(base64_images, filename, self.path_to_output)



