import os
import gradio as gr
import cohere


COHERE_KEY = os.getenv('COHERE_KEY')
co = cohere.Client(COHERE_KEY)

#list_history = [["question", "answer"], ["how", "how what..."]]
def convert_history(list_history):
    """
    Applies the prompt.
    Converts the chat history structure taken by Gradio to the structure suitable for Cohere.
    """
    chat_history = [
        {"role": "SYSTEM", "text": open("prompt.md","r",encoding="UTF-8").read()}
    ]
    for item in list_history:
        dict_chat = {"role": "USER", "text": item[0]}
        chat_history.append(dict_chat)
        dict_chat = {"role": "CHATBOT", "text": item[1]}
        chat_history.append(dict_chat)
    return chat_history
        



def reply(message:str, history:list):
    """
    Takes the input message of the user and chat history and streams the reply of the chatbot.
    """
    chat_history = convert_history(history)
    response = co.chat_stream(
        message=message,
        chat_history=chat_history,
        model="command-nightly",
        temperature=0.25
    )
    text_so_far = ""
    for event in response:
        if event.event_type == 'text-generation':
            text_so_far += event.text
            yield text_so_far


description = """
Hello! 
💬 Use the text box below to ask questions the Technorama 2024 conference!
<nobr> 🗣️ Talk to me in English, Dutch, or French. </nobr>
<nobr> 🔗 [This chatbot was made by Alfiya  Khabibullina](https://www.linkedin.com/in/alfiya-khabibullina-7b13131b8/) </nobr>
"""

gr.ChatInterface(reply,
    title="Technorama Assistant",
    description=description
).launch()