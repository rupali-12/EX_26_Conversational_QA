# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# import os
# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model=genai.GenerativeModel("gemini-pro")
# chat=model.start_chat(history=[])

# def get_gemini_response(question):
#     response=chat.send_message(question, stream=True)
#     return response

# st.set_page_config(page_title="Q&A Demo")
# st.header("Gemini LLM Application")

# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []

# input = st.text_input("Input: ", key = "input")
# submit = st.button("Ask the question")

# if submit and input:
#     response = get_gemini_response(input)
#     # get_gemini_response = get_gemini_response(input)
#     st.session_state['chat_history'].append(["You", input])
#     st.subheader("The Response is")
#     for chunk in response:
#         st.write(chunk.text)
#         st.session_state['chat_history'].append(["Bot", chunk.text])

# st.subheader("The chat history is")

# for role, text in st.session_state['chat_history']:
#     st.write(f"{role}:{text}")



# *******************************************************************************************************
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model and chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

# Streamlit page configuration
st.set_page_config(page_title="Gemini LLM Q&A", layout="wide")

# Page header
st.title("Gemini Conversational Q&A Application")

# Ensure session state initialization
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

# Sidebar configuration
st.sidebar.header("Options")
st.sidebar.text("This is a Q&A interface for interacting with the Gemini LLM.")

# Custom CSS for styling
st.markdown("""
    <style>
    .stTextInput>div>input {
        background-color: #f0f0f0; /* Light gray background */
        color: #000000; /* Black text */
        border: 2px solid #000000; /* Black border */
        border-radius: 4px;
        padding: 10px;
        width: 100%;
    }
    .stTextInput>div>input:focus {
        border-color: #00ff00; /* Green border on focus */
    }
    </style>
    """, unsafe_allow_html=True)

# Chat history container
st.subheader("Chat History")
history_container = st.container()

# Input and submit button
input_container = st.container()
with input_container:
    user_input = st.text_input("Ask your question:", key="input", value=st.session_state['user_input'])
    submit_button = st.button("Submit Question")

# Handle submission
if submit_button and user_input:
    response = get_gemini_response(user_input)
    st.session_state['chat_history'].append(["You", user_input])
    st.session_state['user_input'] = ""  # Clear input field after submission
    
    # Display the response
    st.subheader("Response")
    if response:
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(["Bot", chunk.text])
    else:
        st.write("No response from the model.")

# Display chat history
with history_container:
    if st.session_state['chat_history']:
        for role, text in st.session_state['chat_history']:
            if role == "You":
                st.markdown(f'<div style="background-color:#d4edda;border:1px solid #c3e6cb;border-radius:8px;padding:10px;margin:5px;">**You:** {text}</div>', unsafe_allow_html=True)
            elif role == "Bot":
                st.markdown(f'<div style="background-color:#e2e3e5;border:1px solid #d6d6d6;border-radius:8px;padding:10px;margin:5px;">**Bot:** {text}</div>', unsafe_allow_html=True)
    else:
        st.write("No chat history yet.")

# Additional information
st.sidebar.write("### About")
st.sidebar.write("This application uses Google Gemini to generate responses. Type your questions and get answers in real-time.")
