from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        ##convert the PDF to Image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")  

## Streamlit App

st.set_page_config(page_title="Application Tracking System")
st.header("JOB FIT ANALYZER")
st.subheader("Note:This Application helps you in your Resume Review with help of Google GEMINI Pro Vision Model[LLM]")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])
if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")
submit5 = st.button("Suggest Suitable Jobroles to Apply")
left_col, right_col = st.columns([1, 1])  # You can adjust the width ratio here

with left_col:
     submit1 = st.button("Tell me About the Resume")# Add the buttons on the left side
     submit2 = st.button("How Can I Still Improve My Skills")
   

with right_col:
    # Add the buttons on the right side
    submit3 = st.button("What are the Keywords That are Missing")
    submit4 = st.button("Percentage Match")

user_question = st.text_input("Enter your question here:")

# Button to submit the question
if st.button("Get Answer"):
    if user_question:
        pdf_content = input_pdf_setup(uploaded_file) if uploaded_file else None
        ai_response = get_gemini_response(user_question, pdf_content, input_text)
        st.subheader("The Answer is:")
        st.write(ai_response)
    else:
        st.write("Please enter a question to ask....")

input_prompt1 = """
  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""

input_prompt2 ="""You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to give suggestions to still improve the skills from the provided resume."""

input_prompt3 ="""You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to give the keywords which are missing in the provided resume.""" 

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts."""
 
input_prompt5 = """
"You are an advanced AI job search assistant. Your task is to analyze the provided resume and identify suitable job roles based on the candidate's skills, experience, and education. Please search for relevant job listings that match the candidate's qualifications and profile. 
Ensure the job results are well-aligned with the resume and highlight any positions that would be a strong fit for the candidate's career growth."""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
    
elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit5:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt5,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")