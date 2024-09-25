from embed_data import RagBasedBot, Mode
import os
import gradio as gr


def ask(question:str, history=[["", ""]]):
    
    response = bot.retrieve_answer(question)
    return response
    

bot = None 
history = ""

def main():
    global bot, history
    history = []
    
    current_directory = os.path.dirname(__file__)
    data_path = os.path.join(current_directory, "./data")
    data_base_path = os.path.join(current_directory, "./index_store")
    bot = RagBasedBot(Mode.RETRIEVE, data_path, data_base_path,"gpt-4o")

    #while True:
    #    prompt = input("/n/nQué pregunta tienes (o Enter para salir): ")
    #    if prompt == "":
    #        break
    #    response = bot.retrieve_answer(prompt)
    #    print(response)
        
        
    ui = gr.ChatInterface(fn=ask, textbox=gr.Textbox(placeholder="Soy <Tag> y puedes preguntar sobre reglamentos y procedimientos de la facultad, asi como también sobre las materias de Diseño de Aplicaciones 1 y Fundamentos de ingeniería", container=True, max_lines=10), title="Tag - el chatbot de la cátedra de IngSoft",
                          examples=["¿Qué se dicta en diseño de aplicaciones 1 (DA1)?", "¿Qué se dicta en Fundamentos de Ingeniería de Software (FIS)?", "¿Qué es un obligatorio?", "¿Como se aprueba un parcial de una materia?", "¿Que significa el resultado NSP?", "Como aviso de una suplencia docente"],
                           clear_btn="Clear",retry_btn=None, undo_btn=None)
    ui.launch(share=True)
    

if __name__ == "__main__":
    main()