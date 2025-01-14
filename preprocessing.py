# preprocessing.py
import re
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv
import os
import io

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB')]
fs = gridfs.GridFS(db)

def extract_text_from_pdf(file_stream):
    return extract_pdf_text(file_stream)

def extract_text_from_docx(file_stream):
    doc = Document(file_stream)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

def save_file_to_db(file):
    file_id = fs.put(file.getvalue(), filename=file.name)
    return file_id

def extract_text(file):
    # Save the uploaded file to MongoDB
    file_id = save_file_to_db(file)
    
    # Retrieve the file from MongoDB
    file_stream = fs.get(file_id).read()
    file_extension = file.name.split('.')[-1]
    
    # Extract text based on file extension
    if file_extension == 'pdf':
        text = extract_text_from_pdf(io.BytesIO(file_stream))
    elif file_extension == 'docx':
        text = extract_text_from_docx(io.BytesIO(file_stream))
    else:
        raise ValueError('Unsupported file type.')
    
    return preprocess_text(text)
