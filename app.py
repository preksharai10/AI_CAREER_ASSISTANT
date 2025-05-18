import streamlit as st
import requests
from fpdf import FPDF

st.set_page_config(page_title="GenAI Career Assistant", layout="centered")
st.title(" AI-Powered Career Assistant")

FASTAPI_URL = "https://ai-career-assistant-2v1o.onrender.com"

# Step 1: Select Career Goal
st.subheader("Step 1: Choose Your Career Goal")
career_options = []
with st.spinner("Fetching career options..."):
    try:
        res = requests.get(f"{FASTAPI_URL}/career_options/")
        if res.status_code == 200:
            career_options = res.json().get("career_options", [])
    except Exception:
        st.error(" Failed to fetch career options. Make sure FastAPI is running.")

career_goal = st.selectbox("Select a career path:", career_options)

# Step 2: Upload Resume
st.subheader("Step 2: Upload Your Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# Step 3: Analyze Resume
if st.button(" Analyze Resume and Get Career Plan"):
    if not uploaded_file or not career_goal:
        st.warning("Please upload a resume and select a career goal.")
    else:
        with st.spinner("Analyzing your resume with Gemini..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            data = {"career_goal": career_goal}
            try:
                response = requests.post(f"{FASTAPI_URL}/analyze/", files=files, data=data)
                if response.status_code == 200:
                    result = response.json().get("response", "")

                    st.markdown("---")
                    st.markdown(result, unsafe_allow_html=True)

                    # Extract name
                    name = "Candidate"
                    for line in result.split("\n"):
                        if "**Full Name**" in line:
                            name = line.split(":")[-1].strip()
                            break
                    st.success(f"Hi {name}, here’s your personalized plan!")

                    # Create PDF for download
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_font("Arial", size=12)
                    for line in result.split("\n"):
                        pdf.multi_cell(0, 10, txt=line)
                    pdf_bytes = pdf.output(dest='S').encode('latin1')

                    st.download_button(
                        label=" Download Career Plan as PDF",
                        data=pdf_bytes,
                        file_name="career_plan.pdf",
                        mime="application/pdf"
                    )
                else:
                    error_msg = response.json().get("error", "Unknown error.")
                    st.error(f"Analysis failed: {error_msg}")
            except Exception as e:
                st.error(f" Failed to connect to backend: {e}")
