import sqlite3
import os
from enum import Enum
from datetime import datetime
from typing import List, Dict, Any


def create_metadata_schema():
    current_directory = os.path.dirname(__file__)
    db_path = os.path.join(current_directory, "./db")
    db_file = db_path + "/datasources.db"

    connection = sqlite3.connect(db_file)

    with sqlite3.connect(db_file) as connection:

        # Create a cursor object
        cursor = connection.cursor()

        # Write the SQL command to create the metadata source table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS MetadataSource (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            internal_source_URL TEXT NOT NULL,
            real_source_URL TEXT NOT NULL,
            retrieval_date TEXT NOT NULL,
            source_name TEXT NOT NULL,
            chunk_size INTEGER DEFAULT 256,
            chunk_overlaps INTEGER DEFAULT 20
        );
        '''

        # Execute the SQL command
        cursor.execute(create_table_query)
        # Commit the changes
        connection.commit()
        print("Record inserted successfully!")

def add_metadata():
    current_directory = os.path.dirname(__file__)
    db_path = os.path.join(current_directory, "./db")
    db_file = db_path + "/datasources.db"
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_path = os.path.join(current_directory, "./DataSources/Catedra")

    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()

        # Insert a record into the Students table
        insert_query = '''
            INSERT INTO metadatasource (category, sub_category, internal_source_URL, real_source_URL, retrieval_date, source_name) VALUES
            (?, ?, ?, ?, ?, ?);
        '''

        data = [
            ('Cátedra', 'Acuerdos', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/Catedra/Acuerdos del curso_DA1.docx', 'https://fi365.sharepoint.com/:w:/s/DiseodeAplicaciones1/Eem2F3XrcPNFlw9fZ1rCq9QBeEl48wesLq23VeJo-FQCjA?e=blDNl5', today, 'Acuerdos del curso_DA1.docx'),
            ('Cátedra', 'Información', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/Catedra/0_Descripcio Curso Diseño de aplicaciones 1.docx', 'https://fi365.sharepoint.com/:w:/s/DiseodeAplicaciones1/EVE27wjrKY9EnE9lcV-4QzwBe0Q2K3ImpF-7wqTIcdjt6Q?e=g83OJo', today, '0_Descripcio Curso Diseño de aplicaciones 1.docx'),
            ('Cátedra', 'Información', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/Catedra/1_Temario Teorico Diseño de aplicaciones 1.docx', 'https://fi365.sharepoint.com/:b:/s/DiseodeAplicaciones1/EVuFL6093mBCg0RzSJEvAJ8BtGFPZiJpfFB5FkF6cGiyrQ?e=dG61Pd', today, '1_Temario Teorico Diseño de aplicaciones 1.docx'),
            ('Reglamento', 'Docentes', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/Reglamentos/reglamento-docente__documento-235.pdf', 'https://www.ort.edu.uy/innovaportal/file/95484/1/reglamento-docente__documento-235.pdf', today, 'reglamento-docente__documento-235.pdf'),
            ('Reglamento', 'Facultad', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/Reglamentos/pautas-generales-de-actividad-docente-y-gestion-de-catedras__documento-1041.pdf', 'https://www.ort.edu.uy/innovaportal/file/95484/1/pautas-generales-de-actividad-docente-y-gestion-de-catedras__documento-1041.pdf', today, 'pautas-generales-de-actividad-docente-y-gestion-de-catedras__documento-1041.pdf'),
            ('Template', 'Facultad', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/TemplatesFI/Planilla para Obligatorio EI 0924.docx', 'https://fi365.sharepoint.com/:w:/s/IngSoft_Docentes402/Ee-AuWx6d8FDlps_hONmI0gB-BtNmSYaHDwoVzHZIZNvuA?e=0gpbeB', today,'Planilla para Obligatorio EI 0924.docx'),
            ('Template', 'Facultad', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/TemplatesFI/FORMULARIO SUPLENCIA DOCENTE.docx', 'https://fi365.sharepoint.com/:w:/s/IngSoft_Docentes402/EThbs3nuc2BDksP6qoJkw0AB_qDyR4liopLjvTTDQSihHg?e=AAHn0j', today,'FORMULARIO SUPLENCIA DOCENTE.docx'),       
            ('Template', 'Facultad', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/TemplatesFI/Plantilla para envío de parciales y exámenes_FI.docx', 'https://fi365.sharepoint.com/:w:/s/IngSoft_Docentes402/EcNp4_bbjytJj4dEGGQVf2gBj9c8I5cUFw-dRFo3p-A8gg?e=iQn0Sc', today,'Plantilla para envío de parciales y exámenes_FI.docx')
        ]
        
        cursor.executemany(insert_query, data)


        # Commit the changes
        connection.commit()
        # No need to call connection.close(); it's done automatically!
        print("Record inserted successfully!")
        
def read_metadata_from_db() -> Dict[str, Any]:
    current_directory = os.path.dirname(__file__)
    db_path = os.path.join(current_directory, "./db")
    db_file = db_path + "/datasources.db"

    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()

        select_query = "SELECT * FROM metadatasource;"
        
        cursor.execute(select_query)

        metadata = cursor.fetchall()
        
        metadata_keys = ['id', 'category', 'sub_category', 'internal_source_URL', 'real_source_URL', 'retrieval_date', 'source_name']
        
        metadata_dict = [dict(zip(metadata_keys, record)) for record in metadata]
        
        for record in metadata_dict:
            print(record)

        # No need to call connection.close(); it's done automatically!
        print("Records read successfully!")
        
        return metadata_dict

class DbOperation(Enum):
    SCHEMA = 1
    POPULATE = 2
    READ = 3
   
def main():
    while True:
        print("seleccione la ops de db:")
        op = input()
        if not op.isnumeric():
            print("\n Opción inválida")
            continue
        
        op = int(op)
        if op < 0 or op > 3:
            print("\n Opción inválida")
            continue
        
        if op == 0:
            break
            
        if op == DbOperation.SCHEMA.value:
            create_metadata_schema()
        elif op == DbOperation.POPULATE.value:
            add_metadata()
        elif op == DbOperation.READ.value:
            read_metadata_from_db()

if __name__ == "__main__":
    main()
