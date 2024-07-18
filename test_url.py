#test_url.py
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import fitz  # PyMuPDF
import docx
from bs4 import BeautifulSoup
import requests
import re
import os
import io  # Add this import statement
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Path to the credentials JSON file
CREDENTIALS_FILE = "C:/Users/acer/Downloads/credentials.json"
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Function to authenticate Google Drive API
def authenticate_gdrive():
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

# Function to list files in a folder
def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query).execute()
    return results.get('files', [])

# Function to download a file from Google Drive
def download_file(service, file_id, file_name, save_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(os.path.join(save_path, file_name), 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

# PDF Extraction using PyPDF2
from PyPDF2 import PdfFileReader

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfFileReader(f)
            text = ""
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return ""

# DOCX Extraction
# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from DOCX {docx_path}: {e}")
        return ""

# URL Extraction
# Function to extract text from a URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Error extracting text from URL {url}: {e}")
        return ""

# Text Cleaning
# Function to clean text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    return text.strip().lower()

# Extract and clean text from files
# Function to extract and clean text from downloaded files
def extract_and_clean_text(downloaded_files, save_path):
    all_texts = []
    for file_name in downloaded_files:
        text = ""  # Initialize text to an empty string
        file_path = os.path.join(save_path, file_name)
        
        if file_name.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_name.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif file_name.endswith('.txt'):
            with open(file_path, 'r') as f:
                text = f.read()
        else:
            print(f"Unsupported file type: {file_name}")
            continue  # Skip unsupported file types

        cleaned_text = clean_text(text)
        all_texts.append(cleaned_text)
    return all_texts

# Load pre-trained embedding model
# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to generate sentence embeddings
def generate_embeddings(text_list):
    return model.encode(text_list, show_progress_bar=True)

# Create a FAISS index
# Function to create a FAISS index
def create_faiss_index(embeddings):
    d = embeddings.shape[1]  # Dimension of embeddings
    index = faiss.IndexFlatL2(d)  # L2 distance index
    index.add(embeddings)
    return index

# Function to perform similarity search using FAISS
# Function to perform similarity search using FAISS index
def search_faiss(index, query, model, k=5):
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, k)
    return indices, distances

# Streamlit app
# Streamlit UI layout and functionality
st.set_page_config(page_title="Futuristic Chatbot", page_icon=":robot_face:", layout="wide")

# Custom CSS for futuristic theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #111111;
        color: #FFFFFF;
    }
    .st-bj {
        color: #FFFFFF;
    }
    .st-bk {
        background-color: #1A1A1A;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .st-bh {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
        background-color: #1A1A1A;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to authenticate Google Drive API
service = authenticate_gdrive()

# Define folder ID for Google Drive folder
folder_id = '1X9vP_AmtpnQaJUZN429CTwgr99gMg3JS'  # Update with your folder ID

# List files in the specified Google Drive folder
files = list_files_in_folder(service, folder_id)

# Download files from Google Drive
save_path = './downloads'
os.makedirs(save_path, exist_ok=True)
downloaded_files = []
for file in files:
    download_file(service, file['id'], file['name'], save_path)
    downloaded_files.append(file['name'])

# Extract and clean text from downloaded files
all_texts = extract_and_clean_text(downloaded_files, save_path)

# Generate sentence embeddings using SentenceTransformer model
embeddings = generate_embeddings(all_texts)

# Convert embeddings to numpy array
embeddings = np.array(embeddings).astype('float32')

# Create FAISS index from embeddings
index = create_faiss_index(embeddings)

# Streamlit app UI components
# Streamlit app interface components
st.title('Futuristic Chatbot with Custom Input Data')
st.markdown("---")

query = st.text_input('Enter your query:')
if query:
    indices, distances = search_faiss(index, query, model)
    st.markdown("### Search Results:")
    for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
        st.markdown(f"#### Result {i + 1}:")
        st.write(f"File: {downloaded_files[idx]}")
        st.write(f"Distance: {dist}")
        st.write(f"Text: {all_texts[idx][:500]}")  # Print the first 500 characters of the matched text for brevity
