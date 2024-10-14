import sqlite3
import os
from datetime import datetime

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
    
    
    