**Gemini Voice-Enabled Chatbot with PostgreSQL Persistence**

A multimodal AI chatbot interface built with Python, Gradio, and Google Gemini 1.5 Flash. This application allows users to interact via text or voice and automatically logs all conversations into a PostgreSQL database.

**🚀 Features**
Multimodal Input: Supports both standard text entry and voice-to-text using the SpeechRecognition library.

AI-Powered: Utilizes the gemini-2.5-flash model for fast, intelligent responses.

Database Integration: Uses a ThreadedConnectionPool with PostgreSQL to save user prompts and bot responses in real-time.

Web UI: A clean, responsive interface powered by Gradio.

Error Handling: Robust checks for empty inputs, API failures, and database connection issues.

**🛠️ Prerequisites**

Before running the application, ensure you have the following installed:

->Python 3.9+

->PostgreSQL (running locally or remotely)

->Google Gemini API Key (Get it from Google AI Studio)
