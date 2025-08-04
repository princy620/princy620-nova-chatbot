import streamlit as st
import google.generativeai as genai
from datetime import date
import os
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_api_key")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# Streamlit page setup
st.set_page_config(page_title="NovaChatBot 🎙️", page_icon='🤖', layout='centered')

# Title
st.markdown("<h2 style='text-align: center; color: white; background-color: #232526; border-radius: 10px;'>🤖 NovaChatBot with Voice</h2>", unsafe_allow_html=True)

# Session setup
if 'chat' not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.history = []

if 'today_date' not in st.session_state:
    st.session_state.today_date = date.today().strftime("%d %B %Y")

# New Professional Background & CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
        background-size: cover;
        color: white;
    }
    .user-message {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        max-width: 80%;
        align-self: flex-end;
        background-color: #4caf50;
        color: white;
    }
    .bot-message {
        border-radius: 10px;
        align-self: flex-start;
        padding: 10px;
        margin: 5px 0;
        max-width: 80%;
        background-color: #ffffffd9;
        border: 1px solid #e5e5e5;
        color: black;
    }
    .chat-date {
        text-align: center;
        border-radius: 15px;
        width: 140px;
        background-color: #F0F0F0;
        margin: -15px auto;
        padding: 5px;
        font-weight: bold;
        color: black;
    }
    .message-container {
        display: flex;
        flex-direction: column;
    }
</style>
""", unsafe_allow_html=True)

# Display chat date and history
st.markdown(f'<div class="chat-date">{st.session_state.today_date}</div>', unsafe_allow_html=True)
for msg in st.session_state.history:
    st.markdown(f'<div class="message-container"><div class="user-message">{msg["user"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="message-container"><div class="bot-message">{msg["bot"]}</div></div>', unsafe_allow_html=True)

# Add to chat history
def add_message(user, bot):
    st.session_state.history.append({"user": user, "bot": '🤖\n\n' + bot})

# Handle question from input or voice
def handle_question(question):
    try:
        response = st.session_state.chat.send_message(question)
        add_message(question, response.text)
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Voice input
def listen_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("⚠️ Couldn't understand.")
    except sr.RequestError as e:
        st.error(f"🛑 Mic error: {e}")
    return None

# Input field with voice icon button
col1, col2 = st.columns([8, 1])
with col1:
    question = st.chat_input("Type your message here...")

with col2:
    if st.button("🎤", help="Speak instead"):
        voice_input = listen_microphone()
        if voice_input:
            handle_question(voice_input)
            st.rerun()

# Process chat input (Enter key)
if question:
    handle_question(question)
    st.rerun()
