# classify.py
import torch
from transformers import AlbertTokenizer, AlbertForSequenceClassification
from preprocessing import preprocess_text  # Make sure to import preprocess_text function as well.
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load the model and tokenizer from Hugging Face model hub
tokenizer = AlbertTokenizer.from_pretrained(os.getenv('HUGGINGFACE_MODEL_NAME'))
model = AlbertForSequenceClassification.from_pretrained(os.getenv('HUGGINGFACE_MODEL_NAME'))

def is_valid_resume(text):
    # Check if the resume text is not empty and has a minimum length
    return text.strip() != '' and len(text.split()) > 50


def predict(combined_text):
    if not is_valid_resume(combined_text):
        return 'Invalid resume content. Please provide a complete resume.', 0
    inputs = tokenizer(combined_text, return_tensors='pt', truncation=True, padding=True, max_length=512)  # Adjust max_length if needed.
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return torch.argmax(probs).item(), probs
