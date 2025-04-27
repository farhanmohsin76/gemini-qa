import os
import glob
from pathlib import Path
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

from config import model
from src.utils import extract_csv_content, save_uploaded_file

# Optional: Consider using a more secure secret management solution for the API key
load_dotenv()
#genai.configure(api_key=os.getenv("AIzaSyDXXW8d2jrMWyQ2RfK1tfzq8c-l3sk144Q"))
GEMINI_API_KEY = "AIzaSyDXXW8d2jrMWyQ2RfK1tfzq8c-l3sk144Q"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def main():
    """
    The main function of the Streamlit app.
    """

  # Title
st.title("Natural Language Generation using Annual Financial Report Data using Large Language Model (Gemini 1.5 Flash)")

save_directory = "data"  # Directory to save or check for the file
os.makedirs(save_directory, exist_ok=True)

# Check if a file already exists in the data directory
existing_files = glob.glob(os.path.join(save_directory, "*.csv"))

if existing_files:
    saved_file_path = existing_files[0]  # Use the first found CSV file
   # st.success(f"Using existing file: {os.path.basename(saved_file_path)}")
else:
    uploaded_file = st.file_uploader("Syed Farhan Mohsin", type=["csv"])
    if uploaded_file is not None:
        saved_file_path = save_uploaded_file(uploaded_file, save_directory)
    else:
        st.warning("Please upload a data file to continue.")
        st.stop()  # Stop execution until a file is uploaded

# Proceed with reading and interacting with the file
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": extract_csv_content(saved_file_path)
        }
    ]
)

user_question = st.text_input("Ask your competency questions here")
if user_question:
    response = chat_session.send_message(user_question)
    st.write(response.text)


if __name__ == "__main__":
    main()
