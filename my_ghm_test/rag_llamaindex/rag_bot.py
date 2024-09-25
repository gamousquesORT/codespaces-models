from embed_data import RagBasedBot, Mode
import os
import gradio as gr


def ask(question):
    
    response = bot.retrieve_answer(question)
    return response
    

bot = None 
    
def main():
    global bot
    
    current_directory = os.path.dirname(__file__)
    data_path = os.path.join(current_directory, "./data")
    data_base_path = os.path.join(current_directory, "./index_store")
    bot = RagBasedBot(Mode.RETRIEVE, data_path, data_base_path,"gpt-4o-mini")

    #while True:
    #    prompt = input("/n/nQué pregunta tienes (o Enter para salir): ")
    #    if prompt == "":
    #        break
    #    response = bot.retrieve_answer(prompt)
    #    print(response)
        
        
    ui = gr.Interface(fn=ask, inputs= ["text"], outputs=["text"])
    ui.launch(share=True)
    

if __name__ == "__main__":
    main()