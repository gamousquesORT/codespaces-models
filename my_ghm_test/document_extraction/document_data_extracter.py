from openai import OpenAI
import dotenv
import os
import io
from PIL import Image
import base64
import json
import fitz  # PyMuPDF


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
            base64_image = self._encode_image(temp_image_path)
            base64_images.append(base64_image)

        for temp_image_path in temp_image_paths:
            os.remove(temp_image_path)

        return base64_images
    
    
    def extract_invoice_data(self, base64_image):
            system_prompt = f"""
            You are an OCR-like data extraction tool that extracts events like data from PDFs tabular data calendar.
        
            1. Please extract the data in this events table, written in spanish, by grouping data according to "Mes", "Día" and "Evento", and then output into JSON.

            2. Please keep the keys and values of the JSON in the original language. 

            3. The type of data you might encounter in the table includes but is not limited to a header with: "Mes" like "AGOSTO 2024" , a "descripción" like "Calendario de eventos" or "LAS ENTREGAS ", a Program of Study like "Ingeniería en Sistemas", 
            REUISITO
            
            4. After the header there is a table with the following columns. "Mes", "Día", "Evento", and "Sem". These columns repeate twice in the table.
            for each row in the table, the data might include information about "Mes", "día" , "evento" and "Sem". 
              for example 
                  a combined cell with "Mes" that is a month that runs across severals
                  on each row, in the second column the value of "Día". for example 19 
                  on each row de value of "Evento". for example Comienzo de semestre
                  on each row de value of "Sem". for example 1 meaning the first week of the semester
                  
            following there is a text drawn example of the first week of the semester
             
             ----------------------------
             | Mes | Día | Evento | Sem |
             |-----|-----|--------|-----|
             |    | 19  | Comienzo de semestre |  |
             |    | 20  |                      |  |
             |A    | 21  |                     | 1 |
             |G    | 22  |  Examen DA1         |  |
             |O    | 23  |                     |  |
             |S    |     |                     |   |
             |T    | 26  |                     |  |
             |O    | 27  |                     |  |
             |     | 28  |                     |  |
             |     | 29  |                     | 2 |
             |     | 30  |                     |  |
             |     |     |                     |  |
             |S    | 2   |                     |  |
             |E    | 3   |                     |  |
             |T    | 4   |                     | 3|
             |I    | 5   |                     |  |
             |E    | 6   |                     |  |
                
                
             
            
            5. Don't interpolate or make up data.
            6. Ignore rows with blank values.
            7. Please capture all of the rows and columns in the JSON object.

            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={ "type": "json_object" },
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "extract the data in calendar of eventos and output into JSON "},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}}
                        ]
                    }
                ],
                temperature=0.0,
            )
            return response.choices[0].message.content
    
    
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
        for filename in os.listdir(self.path_to_documents)[:3]:
            file_path = os.path.join(self.path_to_documents, filename)
            print(f"Extracting data from {file_path}")
            if os.path.isfile(file_path):
                base64_images = self.pdf_to_base64_images(file_path)
                self.extract_from_multiple_pages(base64_images, filename, self.path_to_output)