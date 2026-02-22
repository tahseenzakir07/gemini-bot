import google.generativeai as genai #type:ignore
import gradio as gr #type:ignore
import speech_recognition as sr #type:ignore
import os
from psycopg2 import pool # type: ignore

API_KEY = "your_apikey" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

recognizer = sr.Recognizer()

connection_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    dbname="dbname",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)

def save_to_db(user_input, bot_response):
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute('INSERT INTO chatbot("User Prompt", "Bot Response") VALUES (%s, %s)', (user_input, bot_response))
        conn.commit()
        cur.close()
        connection_pool.putconn(conn)
    except Exception as e:
        print(f"DB Error: {e}")

def chat(user_input, chat_history):
    if not user_input.strip():  # Check if user input is empty or just whitespace
        return chat_history, ""  # Return without calling the model

    try:
        response = model.generate_content(user_input)
        bot_response = response.text
        if not bot_response.strip():  # Check if bot response is empty
            bot_response = "Sorry, the model did not provide a response."
        save_to_db(user_input, bot_response)
    except Exception as e:
        bot_response = f"ERROR: {str(e)}"

    chat_history = chat_history or []
    chat_history.append((user_input, bot_response))
    return chat_history, ""

def transcribe(audio_input):
    if not audio_input:
        return ""
    try:
        with sr.AudioFile(audio_input) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Sorry, unable to comprehend audio"
        except sr.RequestError as e:
            text = f"Speech Recognition Error: {e}"
        os.remove(audio_input)
        return text
    except Exception as e:
        return f"Audio Processing Error: {e}"

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        user_input = gr.Textbox(placeholder="Ask away", show_label=False)
        audio_input = gr.Audio(sources=["microphone"], type="filepath")
        clear_button = gr.Button("Clear Chat")

    user_input.submit(fn=chat, inputs=[user_input, chatbot], outputs=[chatbot, user_input])

    audio_input.change(
        fn=transcribe,
        inputs=[audio_input],
        outputs=[user_input]
    ).then(
        fn=chat,
        inputs=[user_input, chatbot],
        outputs=[chatbot, user_input]
    ).then(
        fn=lambda: None,
        inputs=[],
        outputs=[audio_input]
    )

    clear_button.click(lambda: [], None, chatbot)

demo.launch()
