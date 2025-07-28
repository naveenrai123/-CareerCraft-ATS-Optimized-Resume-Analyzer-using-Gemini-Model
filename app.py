from dotenv import load_dotenv
import streamlit as st 
from streamlit_extras import add_vertical_space as avs

import os 
import PyPDF2
from PIL import Image
import requests
import json

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print(api_key)
                            

def get_gemini_response(input_prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [
            {
                "parts": [{"text": input_prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        res_json = response.json()
        try:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "Error: Unexpected response structure.\n\n" + json.dumps(res_json, indent=2)
    else:
        return f"Error {response.status_code}:\n{response.text}"



def input_pdf_text(uploaded_file):
    reader= PyPDF2.PdfReader(uploaded_file)
    text=''
    for page_num in range(len(reader.pages)):
        page =reader.pages[page_num]
        text+=str(page.extract_text())
    return text

input_prompt="""
As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, DevOps Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess resumes against provided job descriptions. In a fiercely competitive job market, your expertise is crucial in offering top-notch guidance for resume enhancement. Assign precise matching percentages based on the JD (Job Description) and meticulously identify any missing keywords with utmost accuracy.
resume:{text}
description:{jd}

I want the response in the following structure:
The first line indicates the percentage match with the job description (JD).
The second line presents a list of missing keywords.
The third section provides a profile summary.

Mention the title for all the three sections.
While generating the response put some space to separate all the three sections.
"""



# Streamlit UI Configuration
st.set_page_config(page_title="Resume ATS Tracker", layout="wide")
avs.add_vertical_space(4)

# 1. Introduction Section
col1, col2 = st.columns([3, 2])
with col1:
    st.title("CareerCraft")
    st.header("Navigate the Job Market with Confidence!")
    st.markdown("""
    <p style='text-align: justify;'>
    Introducing CareerCraft, an ATS-Optimized Resume Analyzer 🚀 your ultimate solution for optimizing job applications and accelerating career growth. 
    Our innovative platform leverages advanced ATS technology to provide job seekers with valuable insights into their resumes' compatibility with job descriptions. 
    From resume optimization and skill enhancement to career progression guidance, CareerCraft empowers users to stand out in today's competitive job market. 
    Streamline your job application process, enhance your skills, and navigate your career path with confidence. 
    Join CareerCraft today and unlock new opportunities for professional success!
    </p>
    """, unsafe_allow_html=True)

with col2:
    st.image('https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif', use_container_width=True)

avs.add_vertical_space(10)

# 2. Offerings Section
col1, col2 = st.columns([3, 2])
with col2:
    st.header("Wide Range of Offerings")
    st.write('• ATS-Optimized Resume Analysis')
    st.write('• Resume Optimization')
    st.write('• Skill Enhancement')
    st.write('• Career Progression Guidance')
    st.write('• Tailored Profile Summaries')
    st.write('• Streamlined Application Process')
    st.write('• Personalized Recommendations')
    st.write('• Efficient Career Navigation')

with col1:
   img1 = Image.open(r"images/icon2.png")

   st.image(img1, use_container_width=True)

avs.add_vertical_space(10)

# 3. Resume ATS Tracker Section
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<h1 style='text-align: center;'>Embark on Your Career Adventure</h1>", unsafe_allow_html=True)
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            text = input_pdf_text(uploaded_file)
            input_prompt = f"Job Description:\n{jd}\n\nResume Text:\n{text}\n\nAnalyze compatibility and give recommendations."
            response = get_gemini_response(input_prompt)
            st.subheader(response)

with col2:
    img2 = Image.open(r"images/icon3.png")

    st.image(img2, use_container_width=True)

avs.add_vertical_space(10)

# 4. FAQ Section
col1, col2 = st.columns([2, 3])
with col2:
    st.markdown("<h1 style='text-align: center;'>FAQ</h1>", unsafe_allow_html=True)
    
    st.write("**Question:** How does CareerCraft analyze resumes and job descriptions?")
    st.write("""**Answer:** CareerCraft uses advanced algorithms to analyze resumes and job descriptions, identifying key keywords and assessing compatibility between the two.""")

    avs.add_vertical_space(3)

    st.write("**Question:** Can CareerCraft suggest improvements for my resume?")
    st.write("""**Answer:** Yes, CareerCraft provides personalized recommendations to optimize your resume for specific job openings, including suggestions for missing keywords and alignment with desired job roles.""")

    avs.add_vertical_space(3)

    st.write("**Question:** Is CareerCraft suitable for both entry-level and experienced professionals?")
    st.write("""**Answer:** Absolutely! CareerCraft caters to job seekers at all career stages, offering tailored insights and guidance to enhance their resumes and advance their careers.""")

with col1:
    img3 = Image.open(r"images/icon4.png")


    st.image(img3, use_container_width=True)
