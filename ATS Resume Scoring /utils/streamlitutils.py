import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd 
import asyncio
from backend.agents.recomendation_agent import recomendation_agent
from backend.agents.ats_agent import ats_agent
from backend.agents.resume_processingagent import resume_processing_agent
from backend.models.open_ai_model_client import get_model_client    
import json 
model = get_model_client()
import plotly.graph_objects as go

async def autogent_runner(agent,task):
    agent_output = await agent.run(task=task)
    return agent_output

def login_ui(autharization_url):
    st.markdown("<h1 style='text-align: center; color: Black;'>Please Login to Continue</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([18,8,16])




        
    st.markdown(f'''<h4 style='text-align: center; color: grey;'><button  type="button"><a target="_self" style="text-decoration:none ; color: Black;" href="{autharization_url}">LOGIN</a></button></h4>''', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import streamlit as st
def generate_pdf(data: dict):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    style_h = styles["Heading1"]
    style_n = styles["Normal"]

    ats_data = data.get("ATS_response", {})
    total_score = ats_data.get("total_score", 0)

    # --- Header ---
    elements.append(Paragraph("📊 ATS Resume Analysis Report", style_h))
    elements.append(Spacer(1, 12))

    # --- Candidate Info ---
    candidate_name = data.get("resume", {}).get("contact_information", {}).get("name", "Unknown Candidate")
    elements.append(Paragraph(f"<b>Candidate:</b> {candidate_name}", style_n))
    elements.append(Spacer(1, 12))

    # --- Total ATS Score ---
    elements.append(Paragraph(f"<b>Total ATS Score:</b> {total_score}%", style_n))
    elements.append(Spacer(1, 12))

    # --- Skill Presence (Present vs Missing) ---
    elements.append(Paragraph("<b>Skill Presence:</b>", style_n))
    skill_table_data = [["Present Skills", "Missing Skills"]]

    skills_df = pd.DataFrame(ats_data.get("skills", []))
    present_df = skills_df[skills_df['found'] == True][['skill']].sort_values('skill')
    not_present_df = skills_df[skills_df['found'] == False][['skill']].sort_values('skill')
    max_len = max(len(not_present_df), len(present_df))

    for i in range(max_len):
        row = [
            present_df['skill'].iloc[i] if i < len(present_df) else "",
            not_present_df['skill'].iloc[i] if i < len(not_present_df) else ""
        ]
        skill_table_data.append(row)

    skill_table = Table(skill_table_data, hAlign='LEFT')
    skill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    elements.append(skill_table)
    elements.append(Spacer(1, 12))

    # --- Category Scores ---
    elements.append(Paragraph("<b>Category Score Breakdown:</b>", style_n))
    for cat in ats_data.get("category_scores", []):
        elements.append(Paragraph(f"{cat['category_name']}: {cat['score_percentage']}%", style_n))
        elements.append(Paragraph(f"Reason: {cat['reasoning']}", style_n))
        elements.append(Spacer(1, 6))

    # --- Missing Skills (if any) ---
    missing_skills = ats_data.get("missing_skills", [])
    if missing_skills:
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>Missing Skills:</b> {', '.join(missing_skills)}", style_n))

    # --- Recommendations ---
    if "recommendation" in data:
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("<b>Recommendations:</b>", style_n))
        for line in data["recommendation"].split("\n"):
            if line.strip():  # skip empty lines
                elements.append(Paragraph(line.strip(), style_n))
                elements.append(Spacer(1, 4))

    doc.build(elements)
    buffer.seek(0)
    return buffer



def display_resume_analysis(data: dict):
    st.header("📊 Resume Analysis Overview")

    # --- Total Score ---
    # st.metric(label="Total ATS Score", value=f"{data['total_score']}%")
    
    fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=data["total_score"],
    title={"text": "Total ATS Score"},
    domain={"x": [0, 1], "y": [0, 1]},
    gauge={
        "axis": {"range": [0, 100]},  # adjust if your score is 0–100
        "bar": {"color": "royalblue"},
        "steps": [
            {"range": [0, 60], "color": "#ffcccc"},
            {"range": [60, 80], "color": "#fff0b3"},
            {"range": [80, 100], "color": "#ccffcc"},
        ],
        "threshold": {"line": {"color": "red", "width": 4}, "value": data["total_score"]},
    },
))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # --- Skills Match (Horizontal Bar Chart) ---
    # st.subheader("Skill Match Overview")
    # skills_df = pd.DataFrame(data["skills"])
    st.subheader("Skill Match Overview")
    skills_df = pd.DataFrame(data["skills"])
    present_df = skills_df[skills_df['found'] == True][['skill']].sort_values('skill')
    not_present_df = skills_df[skills_df['found'] == False][['skill']].sort_values('skill')

    # Combine into a two-column table
    max_len = max(len(present_df), len(not_present_df))
    combined_df = pd.DataFrame({
        "Present Skills": list(present_df['skill']) + [""] * (max_len - len(present_df)),
        "Not Present Skills": list(not_present_df['skill']) + [""] * (max_len - len(not_present_df))
    })

    st.markdown("### Skill Presence Table")
    st.dataframe(combined_df, use_container_width=True)

    # --- Missing Skills ---
    if data.get("missing_skills"):
        st.warning(f"**Missing Skills:** {', '.join(data['missing_skills'])}")


    # --- Category Scores (Vertical Bar Chart) ---
    st.subheader("Category Score Breakdown")
    category_df = pd.DataFrame(data["category_scores"])
    category_df["weighted_score"] = (category_df["score_percentage"] * category_df["weight"]) / 100

    fig_category = px.bar(
        category_df,
        x="category_name",
        y="score_percentage",
        color="score_percentage",
        text="score_percentage",
        title="Category-wise Score"
    )
    fig_category.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_category, use_container_width=True)

    # --- Reasoning Section ---
    st.subheader("Category Reasoning")
    for _, row in category_df.iterrows():
        st.markdown(f"**{row['category_name']} ({row['score_percentage']}%)***{row['reasoning']}*")


agent_resume = resume_processing_agent(model)


agent_ats = ats_agent(model)
recomendation_agent_ats = recomendation_agent(model)

def resume_agent_fnc():
    if st.session_state["resume"]:
        data = " ".join(st.session_state["resume"])
        resume_agent_output = asyncio.run(autogent_runner(agent_resume,data))# for idx, content in enumerate(pages, start=1):
        #upload to data base 
        return resume_agent_output.messages[-1].content.model_dump()
    
def ats_agent_func(resume_data):
    if  st.session_state["resume"] and st.session_state["job_description"] :
        input_data = {
            "resume": resume_data,
            "job_description": st.session_state["job_description"],}
        input_data = json.dumps(input_data)
        ats_output = asyncio.run(autogent_runner(agent_ats,input_data))
        return ats_output.messages[-1].content.model_dump()

def recomendation_agent_func(ats_data,resume_data):
    if  st.session_state["resume"] and st.session_state["job_description"] :
        input_data = {
            "resume": resume_data,
            "job_description": st.session_state["job_description"],
            "ATS_response" : ats_data,
            }
        input_data = json.dumps(input_data)
        recomendation_agent_output = asyncio.run(autogent_runner(recomendation_agent_ats,input_data))
        return recomendation_agent_output.messages[-1].content
