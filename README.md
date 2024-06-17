# Resume Analyzer

The Resume Analyzer is an advanced tool leveraging the ALBERT Large Language Model (LLM) to evaluate and match resumes against job descriptions. By using state-of-the-art NLP techniques, it provides actionable feedback to job seekers, helping them tailor their resumes for better job fit.

## Features

- **AI-Powered Analysis**: Utilizes a fine-tuned ALBERT model from Hugging Face for precise resume-to-job-description matching.
- **Scalable Data Management**: Integrates MongoDB and GridFS for efficient storage and retrieval of resumes, job descriptions, and user feedback.
- **Interactive Interface**: Built with Streamlit, offering a simple and user-friendly interface for uploading resumes and receiving detailed feedback.
- **Real-Time Feedback**: Provides real-time analysis and feedback, including probabilities and recommendations for improving resume fit.
- **User Feedback Storage**: Collects and stores user feedback to continually improve the system's accuracy and relevance.

## Install dependencies

pip install -r requirements.txt

Set up environment variables:
Create a .env file in the root directory with the following variables

HUGGINGFACE_API_KEY=your_hugging_face_api_key 
HUGGINGFACE_MODEL_NAME=albert-base-v2
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB=resume_analyzer

Run the Streamlit app : streamlit run app.py

## Usage

Upload Resume: Use the interface to upload PDF or DOCX resume files.
Enter Job Description: Input the job description into the provided text area.
Analyze: The app processes the resume and job description, concatenates them, and passes the text to the ALBERT model.
View Results: The model predicts the fit and displays the probabilities and feedback in real-time.
Submit Feedback: Users can provide feedback on the prediction, which is stored in MongoDB.


## Result
The system processes uploaded resumes and job descriptions, concatenates and feeds them to the ALBERT model to predict job fit. The results, along with probabilities, are displayed to the user. Feedback is collected and stored in MongoDB, enhancing future analyses.

## Future Improvements
Model Enhancement: Further fine-tuning with diverse datasets to improve accuracy.
Feature Expansion: Adding more NLP features such as keyword matching and skill extraction.
User Interface Improvements: Enhancing the UI for better user experience.
