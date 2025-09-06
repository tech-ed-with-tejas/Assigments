import streamlit as st
import pandas as pd
from io import BytesIO
from backend.utils.pdf_reader import read_pdf_pages_from_bytes
from utils.auth import get_login_str,get_token,get_username
import matplotlib.pyplot as plt
from utils.streamlitutils import generate_pdf,display_resume_analysis,login_ui,ats_agent_func,resume_agent_fnc,recomendation_agent_func
import base64
import random 
import json 
import os 
import time 
from PIL import Image

# -------------------
# ---- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="Hirescore",
    layout="wide",
    initial_sidebar_state="expanded"
)

from streamlit_google_auth import Authenticate
APP_ENV = os.getenv("APP_ENV", "local")  # local | production
REDIRECT_URI = (
    os.getenv("REDIRECT_URI")
    or ("https://your-production-domain.com/callback" if APP_ENV == "production" else "http://localhost:8501/")
)

authenticator = Authenticate(
    secret_credentials_path='./scrects/auth.json',
    cookie_name='my_cookie_name',
    cookie_key='this_is_secret',
    redirect_uri=REDIRECT_URI,
)
authenticator.check_authentification()

# Display the login button if the user is not authenticated
if not st.session_state.get('connected', False):
    authorization_url = authenticator.get_authorization_url()
    
# Center alignment using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
    """
    <div style="text-align: center;">
        <h1>HireScore</h1>
        <p style="font-size:18px; color:gray;">
            Fast, smart, and recruiter-ready: Your resume deserves a second look.
        </p>
    </div>
    """,
    unsafe_allow_html=True)
        cl1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            img = Image.open("./assets/login.png")
            img = img.resize((430, 350))  # (width, height) in pixels
            st.image(img)

        # st.image("./assets/login.png", use_container_width=True,height=100
        #          )
      

        st.markdown(
            """
            <h2 style="text-align:center;">Login with Google</h2>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="text-align: center;">
                <a href="{authorization_url}" target="_self">
                    <button style="
                        background-color:#4285F4;
                        color:white;
                        border:none;
                        padding:10px 24px;
                        font-size:16px;
                        border-radius:8px;
                        cursor:pointer;
                    ">
                        Continue with Google
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    cl1, cl2, cl3 = st.columns([5, 5, 5])
    with cl2:
        st.title("HireScore")
    # with cl3:
    #     img = Image.open("./assets/login.png")
    #     img = img.resize((230, 150))  # (width, height) in pixels
    #     st.image(img)

    st.markdown(
    """
    <div style="text-align: left; padding: 20px 0;">
        <h1 style="margin:0;">AI ATS Resume Analyzer </h1>
        <p style="font-size: 16px; color: #666;">
            Fast, smart, and recruiter-ready: Your resume deserves a second look.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
 
    # ----------------------- SESSION INIT -----------------------
    if "resume" not in st.session_state:
        st.session_state["resume"] = None

    if "job_description" not in st.session_state:
        st.session_state["job_description"] = None

    # ----------------------- HEADER -----------------------
    # st.title("🤖 ATS Resume Analyzer AI Agent")
    # st.markdown("### Easily compare your resume with job descriptions to get an ATS match score.")

    # ----------------------- SIDEBAR -----------------------
    st.sidebar.title("📂 Resume & Job Selection")

    # --- Resume Upload ---
    uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        try:
            with st.spinner("Reading resume..."):
                st.session_state["resume"] = read_pdf_pages_from_bytes(file_bytes)
            st.sidebar.success("✅ Resume uploaded successfully!")
            
        except Exception as e:
            st.sidebar.error(f"❌ Failed to read PDF: {e}")

    # --- Job Description Selection ---
    st.sidebar.subheader("Select Job Description")
    jd = pd.read_csv('./job_title_des.csv')
    job_titles = jd['Job Title'].unique().tolist()

    selected_job_title = st.sidebar.selectbox("Choose Job Title", job_titles, index=None)

    selected_job_description = None
    if selected_job_title:
        filtered_jd = jd[jd['Job Title'] == selected_job_title]
        
        if len(filtered_jd) > 1:
            selected_index = st.sidebar.selectbox(
                "Select Specific JD", range(len(filtered_jd)), index=None,
                format_func=lambda x: f"JD #{x+1}"
            )
        else:
            selected_index = 0
        
        if selected_index is not None:
            selected_job_description = filtered_jd.iloc[selected_index]["Job Description"]
            st.session_state["job_description"] = selected_job_description
            st.sidebar.success("✅ Job Description loaded!")

    # ----------------------- MAIN AREA -----------------------
    tab1, tab2 = st.tabs([ "📝 Job Description","📄 Resume Preview"])
    with tab1:
        st.subheader("Selected Job Description")
        if selected_job_description:
            st.text_area("Job Description", selected_job_description, height=300)
        else:
            st.info("Please select a Job Title & JD from the sidebar.")
    with tab2:
        st.subheader("Uploaded Resume Content")
        if st.session_state["resume"]:
            base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

            # Display PDF in an iframe
            pdf_display = f"""
            <iframe
                src="data:application/pdf;base64,{base64_pdf}"
                width="100%"
                height="800"
                type="application/pdf"
            ></iframe>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)

        else:
            st.info("Please upload a resume in PDF format.")

    # ----------------------- ACTION AREA -----------------------
    st.markdown("---")
    if st.session_state["resume"] and st.session_state["job_description"]:
        if st.button("🔍 Analyze Resume"):
            with st.spinner("Running ATS analysis..."):
                with st.status("Running…", expanded=True):
                    my_bar = st.progress(0, text="Please wait…")
                    
            
                        # Run the resume agent
                    resume_data = resume_agent_fnc()
                    my_bar.progress(30, text="Resume processing done")
                    # # JD agent skip 
                    # # run ats agent 
                    ats_data = ats_agent_func(resume_data)
                    my_bar.progress(60, text="Generating Scores")
                    # # run recomendation agent
                    recomendation = recomendation_agent_func(ats_data,resume_data)
                    # Display results
                    display_resume_analysis(ats_data)
                    my_bar.progress(90, text="Generating recomendations")
                    time.spleep(10)
                    st.write("### Improvement Recommendations")
                    st.write(recomendation)
                    data = {
                        "resume": resume_data,
                        "job_description": st.session_state["job_description"],
                        "ATS_response": ats_data,
                        "recommendation": recomendation
                    }
                    random_num = random.randint(0, 10)
                    with open(f"test{random_num}.json", "w") as f:
                        f.write(json.dumps(data))
                
                    my_bar.empty()
                st.success("Completed ATS analysis.")
                # with open(f"test8.json", "r") as f:
                #     data = json.load(f)

                pdf_buffer = generate_pdf(data)
                st.download_button(
                    label="📥 Download ATS Report (PDF)",
                    data=pdf_buffer,
                    file_name="ATS_Resume_Analysis.pdf",
                    mime="application/pdf"
                )

    else:
        st.warning("Upload a resume and select a job description to continue.")

    # ----------------------- FOOTER -----------------------
    st.caption("Built with ❤️ using Streamlit")
    if st.sidebar.button('Log out'):
        authenticator.logout()

