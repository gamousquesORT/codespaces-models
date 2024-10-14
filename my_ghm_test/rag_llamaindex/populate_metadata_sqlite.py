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
        source_name TEXT NOT NULL
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
        ('Reglamento', 'Docentes', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/Reglamentos/reglamento-docente__documento-235.pdf', 'https://www.ort.edu.uy/innovaportal/file/95484/1/reglamento-docente__documento-235.pdf', today, 'reglamento-docente__documento-235.pdf'),
        ('Template', 'Cátedra', '/workspaces/codespaces-models/my_ghm_test/rag_llamaindex/DataSources/TemplatesFI/FORMULARIO SUPLENCIA DOCENTE.docx', 'https://fi365.sharepoint.com/:w:/s/IngSoft_Docentes402/EThbs3nuc2BDksP6qoJkw0AB_qDyR4liopLjvTTDQSihHg?e=AAHn0j', today,'FORMULARIO SUPLENCIA DOCENTE.docx')
    ]
    
    cursor.executemany(insert_query, data)


    # Commit the changes
    connection.commit()
    # No need to call connection.close(); it's done automatically!
    print("Record inserted successfully!")
    
    
    