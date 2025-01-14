import streamlit as st
from preprocessing import extract_text, preprocess_text
from classify import predict
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime
import numpy as np

# Load environment variables
load_dotenv()

def save_to_db(resume_text, job_description_text, label, probabilities, feedback):
    # Create a document to insert into the database
    document = {
        "resume_text": resume_text,
        "job_description_text": job_description_text,
        "prediction_label": label,
        "prediction_probabilities": probabilities,
        "user_feedback": feedback,
        "timestamp": datetime.datetime.utcnow()  # Include a timestamp
    }
    
    # Insert the document into a collection called 'predictions'
    db.predictions.insert_one(document)

# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB')]

st.title("Resume Analyzer")

# User input for job description
job_description = st.text_area("Enter the job description here:")

uploaded_file = st.file_uploader("Upload a resume file", type=["pdf", "docx"])

if uploaded_file is not None and job_description:
    with st.spinner('Processing...'):
        # Extract and preprocess text from resume
        resume_text = extract_text(uploaded_file)
        
        # Preprocess job description text
        job_description_text = preprocess_text(job_description)
        
        # Concatenate resume text and job description text
        combined_text = resume_text + " " + job_description_text
        
        # Get predictions
        label, probabilities = predict(combined_text)
        
        # Convert probabilities to a numpy array
        probabilities_array = probabilities.detach().numpy()
    
        # Flatten the array if it's nested and convert to a list
        if probabilities_array.ndim > 1:
            probabilities_list = probabilities_array.flatten().tolist()
        else:
            probabilities_list = probabilities_array.tolist()
        
        # Convert probabilities to percentages
        probabilities_percentages = [prob * 100 for prob in probabilities_list]

        st.success('Done!')
        
        fit_probability = probabilities_percentages[1] if label == 1 else probabilities_percentages[0]
    
        if label == 1:
            st.write("**The candidate is fit for this job.**")
            st.write(f"Probability of being fit: **{probabilities_percentages[1]:.2f}%**")
            
            # Provide feedback based on probability
            if fit_probability > 80:
                st.write("The candidate has strong potential for this role and is highly recommended.")
            elif fit_probability > 50:
                st.write("The candidate has good potential but could improve by customizing the resume to highlight relevant skills and experiences.")
            else:
                st.write("The candidate may need to gain more relevant experience or consider roles that better match their current skill set.")
            
        else:
            st.write("**The candidate is not fit for this job.**")
            st.write(f"Probability of not being fit: **{probabilities_percentages[0]:.2f}%**")
            
            # Provide feedback based on probability
            if fit_probability > 80:
                st.write("The candidate is unlikely to be a good fit for this role and may want to consider different opportunities.")
            elif fit_probability > 50:
                st.write("The candidate could improve their chances by focusing on developing specific skills or gaining more experience in related areas.")
            else:
                st.write("The candidate has some potential but should work on strengthening their resume before applying for similar roles.")

        # Collect user feedback
        feedback = st.text_area("Do you agree with the prediction? Any suggestions for improvement?")
        if st.button('Submit Feedback'):
            # Process and store the feedback
            save_to_db(resume_text, job_description_text, label, probabilities_list, feedback)
            st.write("Thank you for your feedback!")
