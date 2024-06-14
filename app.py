import streamlit as st
import os
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('google_api_key'))

#generatinge model

def get_gemini_res(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

#define pdf as input

def get_input_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=''
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
        return text


#prompt template

input_prompt='''
    Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}

'''

#streamlit app

st.header("SMART ATS")
st.text("Improve your resume")
jd=st.text_area('paste job description')

uploaded_file=st.sidebar.file_uploader("upload yout resume here")


submit=st.button("submit")

if submit:
    if uploaded_file is not None:
        text=get_input_text(uploaded_file)
        response=get_gemini_res(input_prompt)

        st.subheader("The Response is")
        st.write(response)