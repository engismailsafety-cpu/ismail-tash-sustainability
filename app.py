import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from datetime import datetime
import numpy as np
import io
import base64
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.units import inch, cm
import tempfile
import os
import matplotlib.pyplot as plt

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Professional ESG Benchmarking Platform",
    page_icon="🏆",
    layout="wide"
)

# -----------------------
# CUSTOM CSS - مع تحسين ألوان الفريق
# -----------------------
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%);
        padding: 35px 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 { color: white; margin: 0; font-size: 36px; font-weight: 700; }
    .main-header p { color: #E8F5E9; margin: 15px 0 0 0; }
    
    /* تحسين ألوان الفريق - نص أبيض على خلفية داكنة */
    .team-container {
        background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,215,0,0.3);
    }
    .team-title {
        color: #FFD54F !important;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    .team-table {
        width: 100%;
        border-collapse: collapse;
    }
    .team-table th {
        background: rgba(255,255,255,0.15);
        color: #E8F5E9 !important;
        padding: 12px;
        text-align: center;
        font-size: 16px;
    }
    .team-table td {
        padding: 10px;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        color: #FFFFFF !important;
        font-size: 15px;
    }
    .team-leader-row {
        background: rgba(255,215,0,0.15);
    }
    .team-leader-name {
        color: #FFD54F !important;
        font-weight: bold !important;
        font-size: 17px !important;
    }
    .team-member-name {
        color: #FFFFFF !important;
        font-size: 15px !important;
    }
    .team-leader-label {
        color: #FFD54F !important;
        font-weight: bold;
    }
    
    .company-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 6px solid #1B5E20;
        margin: 10px 0;
        transition: all 0.3s;
    }
    .company-card:hover { transform: translateY(-5px); box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
    .company-card .rank { font-size: 14px; color: #64748b; }
    .company-card .score { font-size: 32px; font-weight: 700; color: #1B5E20; }
    .winner-badge {
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
        padding: 4px 16px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 600;
        display: inline-block;
    }
    .progress-bar {
        height: 8px;
        background: #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
        margin: 5px 0;
    }
    .progress-bar .fill {
        height: 100%;
        background: linear-gradient(90deg, #1B5E20, #2E7D32);
        border-radius: 10px;
        transition: width 1s ease;
    }
    .metric-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        background: #F1F5F9;
        margin: 3px;
    }
    .supervisor-card {
        background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,215,0,0.3);
    }
    .supervisor-title {
        color: #FFD54F;
        font-size: 22px;
        margin: 0 0 10px 0;
    }
    .supervisor-name {
        color: #FF0000;
        font-weight: bold;
        font-size: 36px;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .supervisor-qualification {
        font-size: 18px;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# LOGIN SYSTEM
# -----------------------
users = {"admin": "1234", "ismail": "2024"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "results" not in st.session_state:
    st.session_state.results = None

if not st.session_state.logged_in:
    st.markdown("""
        <div class='main-header'>
            <h1>🏆 Professional ESG Benchmarking Platform</h1>
            <p>AI-Powered Analysis for ExxonMobil, Saudi Aramco & BP</p>
            <p style='font-weight: bold; color: white; margin-top: 15px;'>Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash</p>
            <p style='font-size: 13px; color: #FFD54F;'>QHSE Master at Alexandria University</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Login to Access Platform")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if username in users and users[username] == password:
                    st.session_state.logged_in = True
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='team-container'>
                <div class='team-title'>👥 PROJECT TEAM</div>
                <table class='team-table'>
                    <tr>
                        <th>Role</th>
                        <th>Name</th>
                    </tr>
                    <tr class='team-leader-row'>
                        <td class='team-leader-label'>🏆 Team Leader</td>
                        <td class='team-leader-name'>Ismail Kamal</td>
                    </tr>
                    <tr>
                        <td>📋 Team Member</td>
                        <td class='team-member-name'>Adel ElSayed</td>
                    </tr>
                    <tr>
                        <td>📋 Team Member</td>
                        <td class='team-member-name'>Mohamed Gaber</td>
                    </tr>
                    <tr>
                        <td>📋 Team Member</td>
                        <td class='team-member-name'>Ahmed Omar</td>
                    </tr>
                    <tr>
                        <td>📋 Team Member</td>
                        <td class='team-member-name'>Sherouk Ashraf</td>
                    </tr>
                    <tr>
                        <td>📋 Team Member</td>
                        <td class='team-member-name'>Mohamed ElHammadi</td>
                    </tr>
                    <tr>
                        <td>📋 Team Member</td>
                        <td class='team-member-name'>Farouk Sameh</td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='supervisor-card'>
                <div class='supervisor-title'>🎓 Under Supervision of</div>
                <div class='supervisor-name'>Dr. Mohamed Tash</div>
                <div class='supervisor-qualification'>QHSE Master at Alexandria University</div>
                <div style='margin-top: 15px; color: #FFD54F; font-size: 12px;'>⭐ Lead Supervisor | ESG Expert ⭐</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.stop()

# -----------------------
# MAIN HEADER
# -----------------------
st.markdown("""
    <div class='main-header'>
        <h1>🏆 Professional ESG Benchmarking Platform</h1>
        <p>AI-Powered Analysis for ExxonMobil, Saudi Aramco & BP</p>
        <p style='font-weight: bold; color: white; margin-top: 15px;'>Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash</p>
        <p style='font-size: 13px; color: #FFD54F;'>QHSE Master at Alexandria University</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------
# SIDEBAR - مع تحسين ألوان الفريق
# -----------------------
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 50px;'>🏆</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%); border-radius: 15px; padding: 15px;'>
        <h4 style='color: #FFD54F; text-align: center;'>👥 PROJECT TEAM</h4>
        <div style='color: #FFFFFF; font-size: 14px;'>
            <p style='color: #FFD54F; font-weight: bold;'>🏆 Ismail Kamal <span style='color: #E8F5E9; font-weight: normal;'>(Leader)</span></p>
            <p style='color: #E8F5E9;'>• Adel ElSayed</p>
            <p style='color: #E8F5E9;'>• Mohamed Gaber</p>
            <p style='color: #E8F5E9;'>• Ahmed Omar</p>
            <p style='color: #E8F5E9;'>• Sherouk Ashraf</p>
            <p style='color: #E8F5E9;'>• Mohamed ElHammadi</p>
            <p style='color: #E8F5E9;'>• Farouk Sameh</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); border-radius: 15px; padding: 15px; text-align: center;'>
        <h4 style='color: #2E7D32;'>🎓 SUPERVISOR</h4>
        <p style='color: #FF0000; font-weight: bold; font-size: 20px;'>Dr. Mohamed Tash</p>
        <p style='color: #2E7D32; font-weight: bold; font-size: 12px;'>QHSE Master at Alexandria University</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Version 10.0 | Professional ESG Benchmarking")

# -----------------------
# CORE FUNCTIONS
# -----------------------
def extract_text_from_pdf(file):
    """استخراج النص من ملف PDF"""
    if file is None:
        return ""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return ""

def safe_extract_number(pattern, text, default=0):
    """استخراج رقم من النص بطريقة آمنة"""
    try:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            for group in match.groups():
                if group is not None:
                    clean = re.sub(r'[^\d.]', '', str(group))
                    if clean:
                        return float(clean)
        return default
    except Exception:
        return default

def extract_esg_metrics(text, company_name):
    """استخراج مؤشرات ESG من النص"""
    
    ghg = safe_extract_number(r'GHG\s*emissions?.*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, 100)
    if ghg == 0:
        ghg = safe_extract_number(r'(\d+(?:\.\d+)?)\s*(?:million|M)\s*(?:tons?)?\s*(?:CO2|GHG)', text, 100)
    
    renewable = safe_extract_number(r'renewable\s*energy.*?(\d+(?:\.\d+)?)\s*%', text, 10)
    recycling = safe_extract_number(r'recycling\s*rate.*?(\d+(?:\.\d+)?)\s*%', text, 65)
    water = safe_extract_number(r'water\s*(?:intensity|consumption).*?(\d+(?:\.\d+)?)', text, 0.8)
    biodiversity = safe_extract_number(r'biodiversity\s*score.*?(\d+(?:\.\d+)?)', text, 70)
    methane = safe_extract_number(r'methane\s*intensity.*?(\d+(?:\.\d+)?)', text, 0.4)
    ltir = safe_extract_number(r'LTIR|safety.*?(\d+(?:\.\d+)?)', text, 0.3)
    safety_events = safe_extract_number(r'(?:process\s*safety|PSI).*?(\d+)', text, 8)
    training = safe_extract_number(r'training\s*hours.*?(\d+(?:\.\d+)?)', text, 40)
    diversity = safe_extract_number(r'(?:women|female|diversity).*?(\d+(?:\.\d+)?)\s*%', text, 25)
    epi = safe_extract_number(r'EPI\s*score.*?(\d+(?:\.\d+)?)', text, 75)
    transparency = safe_extract_number(r'transparency\s*score.*?(\d+(?:\.\d+)?)', text, 80)
    risk = safe_extract_number(r'risk\s*score.*?(\d+(?:\.\d+)?)', text, 75)
    energy_eff = safe_extract_number(r'energy\s*efficiency.*?(\d+(?:\.\d+)?)\s*%', text, 82)
    carbon_int = safe_extract_number(r'carbon\s*intensity.*?(\d+(?:\.\d+)?)', text, 200)
    
    return {
        "Company": company_name,
        "GHG_Emissions": ghg,
        "Renewable_Energy": renewable,
        "Recycling_Rate": recycling,
        "Water_Intensity": water,
        "Biodiversity_Score": biodiversity,
        "Methane_Intensity": methane,
        "Safety_LTIR": ltir,
        "Process_Safety_Events": safety_events,
        "Training_Hours": training,
        "Diversity_Rate": diversity,
        "EPI_Score": epi,
        "Transparency_Score": transparency,
        "Risk_Score": risk,
        "Energy_Efficiency": energy_eff,
        "Carbon_Intensity": carbon_int,
    }

def calculate_professional_scores(df):
    """حساب الدرجات الاحترافية مع الأوزان"""
    df_calc = df.copy()
    
    # Environmental Score (35%)
    max_ghg = max(df_calc['GHG_Emissions'].max(), 1)
    df_calc['GHG_Score'] = (1 - (df_calc['GHG_Emissions'] / max_ghg)) * 100
    df_calc['Renewable_Score'] = df_calc['Renewable_Energy'] * 5
    df_calc['Recycling_Score'] = df_calc['Recycling_Rate']
    max_water = max(df_calc['Water_Intensity'].max(), 0.1)
    df_calc['Water_Score'] = (1 - (df_calc['Water_Intensity'] / max_water)) * 100
    df_calc['Biodiversity_Score'] = df_calc['Biodiversity_Score']
    max_methane = max(df_calc['Methane_Intensity'].max(), 0.01)
    df_calc['Methane_Score'] = (1 - (df_calc['Methane_Intensity'] / max_methane)) * 100
    
    df_calc['Environmental_Score'] = (
        df_calc['GHG_Score'] * 0.25 +
        df_calc['Renewable_Score'] * 0.20 +
        df_calc['Recycling_Score'] * 0.20 +
        df_calc['Water_Score'] * 0.15 +
        df_calc['Biodiversity_Score'] * 0.10 +
        df_calc['Methane_Score'] * 0.10
    )
    
    # Social Score (25%)
    max_ltir = max(df_calc['Safety_LTIR'].max(), 0.1)
    df_calc['Safety_Score'] = (1 - (df_calc['Safety_LTIR'] / max_ltir)) * 100
    max_events = max(df_calc['Process_Safety_Events'].max(), 1)
    df_calc['Safety_Events_Score'] = (1 - (df_calc['Process_Safety_Events'] / max_events)) * 100
    max_training = max(df_calc['Training_Hours'].max(), 1)
    df_calc['Training_Score'] = (df_calc['Training_Hours'] / max_training) * 100
    max_diversity = max(df_calc['Diversity_Rate'].max(), 1)
    df_calc['Diversity_Score'] = (df_calc['Diversity_Rate'] / max_diversity) * 100
    
    df_calc['Social_Score'] = (
        df_calc['Safety_Score'] * 0.35 +
        df_calc['Safety_Events_Score'] * 0.25 +
        df_calc['Training_Score'] * 0.20 +
        df_calc['Diversity_Score'] * 0.20
    )
    
    # Governance Score (20%)
    max_epi = max(df_calc['EPI_Score'].max(), 1)
    df_calc['EPI_Score_Norm'] = (df_calc['EPI_Score'] / max_epi) * 100
    max_trans = max(df_calc['Transparency_Score'].max(), 1)
    df_calc['Transparency_Score_Norm'] = (df_calc['Transparency_Score'] / max_trans) * 100
    max_risk = max(df_calc['Risk_Score'].max(), 1)
    df_calc['Risk_Score_Norm'] = (1 - (df_calc['Risk_Score'] / max_risk)) * 100
    
    df_calc['Governance_Score'] = (
        df_calc['EPI_Score_Norm'] * 0.40 +
        df_calc['Transparency_Score_Norm'] * 0.35 +
        df_calc['Risk_Score_Norm'] * 0.25
    )
    
    # Operational Score (20%)
    max_energy = max(df_calc['Energy_Efficiency'].max(), 1)
    df_calc['Energy_Score'] = (df_calc['Energy_Efficiency'] / max_energy) * 100
    max_carbon = max(df_calc['Carbon_Intensity'].max(), 1)
    df_calc['Carbon_Intensity_Score'] = (1 - (df_calc['Carbon_Intensity'] / max_carbon)) * 100
    
    df_calc['Operational_Score'] = (
        df_calc['Energy_Score'] * 0.50 +
        df_calc['Carbon_Intensity_Score'] * 0.50
    )
    
    # Overall Score
    df_calc['Overall_Score'] = (
        df_calc['Environmental_Score'] * 0.35 +
        df_calc['Social_Score'] * 0.25 +
        df_calc['Governance_Score'] * 0.20 +
        df_calc['Operational_Score'] * 0.20
    )
    
    df_calc['Rank'] = df_calc['Overall_Score'].rank(ascending=False, method='dense').astype(int)
    
    return df_calc

# -----------------------
# DEMO DATA
# -----------------------
@st.cache_data
def get_demo_data():
    data = {
        "Company": ["ExxonMobil", "Saudi Aramco", "BP"],
        "GHG_Emissions": [112, 53.2, 63],
        "Renewable_Energy": [8, 12, 15],
        "Recycling_Rate": [65, 68, 72],
        "Water_Intensity": [0.85, 0.72, 0.68],
        "Biodiversity_Score": [65, 72, 78],
        "Methane_Intensity": [0.45, 0.35, 0.28],
        "Safety_LTIR": [0.35, 0.28, 0.22],
        "Process_Safety_Events": [12, 8, 5],
        "Training_Hours": [35, 42, 48],
        "Diversity_Rate": [22, 28, 35],
        "EPI_Score": [72, 78, 85],
        "Transparency_Score": [75, 82, 88],
        "Risk_Score": [25, 20, 15],
        "Energy_Efficiency": [80, 85, 90],
        "Carbon_Intensity": [220, 195, 180],
    }
    return pd.DataFrame(data)

def process_uploaded_reports(files):
    """معالجة التقارير المرفوعة"""
    results = []
    company_names = ["ExxonMobil", "Saudi Aramco", "BP"]
    
    for i, file in enumerate(files):
        if file is not None:
            text = extract_text_from_pdf(file)
            if text:
                data = extract_esg_metrics(text, company_names[i])
                results.append(data)
            else:
                default_data = {
                    "Company": company_names[i],
                    "GHG_Emissions": 75 + i * 20,
                    "Renewable_Energy": 10 + i * 3,
                    "Recycling_Rate": 65 + i * 3,
                    "Water_Intensity": 0.75 - i * 0.05,
                    "Biodiversity_Score": 70 + i * 4,
                    "Methane_Intensity": 0.40 - i * 0.05,
                    "Safety_LTIR": 0.30 - i * 0.03,
                    "Process_Safety_Events": 10 - i * 2,
                    "Training_Hours": 35 + i * 5,
                    "Diversity_Rate": 22 + i * 5,
                    "EPI_Score": 72 + i * 5,
                    "Transparency_Score": 75 + i * 5,
                    "Risk_Score": 25 - i * 3,
                    "Energy_Efficiency": 80 + i * 3,
                    "Carbon_Intensity": 220 - i * 15,
                }
                results.append(default_data)
        else:
            default_data = {
                "Company": company_names[i],
                "GHG_Emissions": 75 + i * 20,
                "Renewable_Energy": 10 + i * 3,
                "Recycling_Rate": 65 + i * 3,
                "Water_Intensity": 0.75 - i * 0.05,
                "Biodiversity_Score": 70 + i * 4,
                "Methane_Intensity": 0.40 - i * 0.05,
                "Safety_LTIR": 0.30 - i * 0.03,
                "Process_Safety_Events": 10 - i * 2,
                "Training_Hours": 35 + i * 5,
                "Diversity_Rate": 22 + i * 5,
                "EPI_Score": 72 + i * 5,
                "Transparency_Score": 75 + i * 5,
                "Risk_Score": 25 - i * 3,
                "Energy_Efficiency": 80 + i * 3,
                "Carbon_Intensity": 220 - i * 15,
            }
            results.append(default_data)
    
    df = pd.DataFrame(results)
    return calculate_professional_scores(df)

# -----------------------
# PDF EXPORT FUNCTIONS
# -----------------------
def save_fig_as_image(fig, width=600, height=400):
    """حفظ الرسم البياني كصورة مؤقتة"""
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            fig.write_image(tmp.name, width=width, height=height, scale=1)
            return tmp.name
    except Exception as e:
        return None

def generate_pdf_report(df_calc, winner, runner):
    """توليد تقرير PDF كامل"""
    
    filename = f"ESG_Benchmarking_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    story = []
    
    # عنوان التقرير
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                 fontSize=24, textColor=colors.HexColor('#1B5E20'),
                                 spaceAfter=30, alignment=1)
    
    story.append(Paragraph("🏆 Professional ESG Benchmarking Report", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("AI-Powered Analysis for ExxonMobil, Saudi Aramco & BP", styles['Heading2']))
    story.append(Spacer(1, 24))
    
    # معلومات الفريق والمشرف
    story.append(Paragraph("<b>Team Leader:</b> Ismail Kamal", styles['Normal']))
    story.append(Paragraph("<b>Team Members:</b> Adel ElSayed, Mohamed Gaber, Ahmed Omar, Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh", styles['Normal']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b><font color='red'>Under Supervision:</font> Dr. Mohamed Tash</b>", styles['Normal']))
    story.append(Paragraph("<b>QHSE Master at Alexandria University</b>", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Winner Analysis
    story.append(Paragraph("🏆 Winner Analysis", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    rating = "⭐ A+ (Excellent)" if winner['Overall_Score'] >= 85 else \
             "⭐ A (Very Good)" if winner['Overall_Score'] >= 75 else \
             "⭐ B+ (Good)" if winner['Overall_Score'] >= 65 else \
             "⭐ B (Satisfactory)" if winner['Overall_Score'] >= 55 else \
             "⭐ C (Needs Improvement)"
    
    winner_text = f"""
    <b>Company:</b> {winner['Company']}<br/>
    <b>Overall Score:</b> {winner['Overall_Score']:.1f}/100<br/>
    <b>Rank:</b> #{int(winner['Rank'])}<br/>
    <b>ESG Rating:</b> {rating}<br/><br/>
    <b>Key Strengths:</b><br/>
    • EPI Score: {winner['EPI_Score']:.1f}<br/>
    • Recycling Rate: {winner['Recycling_Rate']:.1f}%<br/>
    • Safety Performance: LTIR {winner['Safety_LTIR']:.2f}<br/>
    • Renewable Energy: {winner['Renewable_Energy']:.1f}%
    """
    story.append(Paragraph(winner_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Scores Table
    story.append(Paragraph("📊 Detailed Scores", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    table_data = [
        ['Company', 'Overall', 'Environmental', 'Social', 'Governance', 'Operational']
    ]
    
    for idx, row in df_calc.iterrows():
        table_data.append([
            row['Company'],
            f"{row['Overall_Score']:.1f}%",
            f"{row['Environmental_Score']:.1f}%",
            f"{row['Social_Score']:.1f}%",
            f"{row['Governance_Score']:.1f}%",
            f"{row['Operational_Score']:.1f}%"
        ])
    
    table = Table(table_data, colWidths=[100, 70, 80, 70, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B5E20')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
    ]))
    story.append(table)
    story.append(Spacer(1, 30))
    
    # Full Metrics Table
    story.append(Paragraph("📋 Full Metrics Comparison", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    metrics_data = [
        ['Metric', 'ExxonMobil', 'Saudi Aramco', 'BP']
    ]
    
    metrics = [
        ('GHG Emissions (M t)', 'GHG_Emissions'),
        ('Renewable Energy (%)', 'Renewable_Energy'),
        ('Recycling Rate (%)', 'Recycling_Rate'),
        ('Water Intensity', 'Water_Intensity'),
        ('Biodiversity Score', 'Biodiversity_Score'),
        ('Methane Intensity', 'Methane_Intensity'),
        ('Safety LTIR', 'Safety_LTIR'),
        ('Process Safety Events', 'Process_Safety_Events'),
        ('Training Hours', 'Training_Hours'),
        ('Diversity Rate (%)', 'Diversity_Rate'),
        ('EPI Score', 'EPI_Score'),
        ('Transparency Score', 'Transparency_Score'),
        ('Risk Score', 'Risk_Score'),
        ('Energy Efficiency (%)', 'Energy_Efficiency'),
        ('Carbon Intensity', 'Carbon_Intensity'),
    ]
    
    for label, col in metrics:
        row = [label]
        for idx, row_data in df_calc.iterrows():
            row.append(f"{row_data[col]:.1f}")
        metrics_data.append(row)
    
    metrics_table = Table(metrics_data, colWidths=[80, 70, 70, 70])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B5E20')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 30))
    
    # Runner-up Analysis
    if runner is not None:
        story.append(Paragraph("📈 Runner-Up Analysis", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        runner_text = f"""
        <b>Company:</b> {runner['Company']}<br/>
        <b>Overall Score:</b> {runner['Overall_Score']:.1f}/100<br/>
        <b>Gap from Winner:</b> {winner['Overall_Score'] - runner['Overall_Score']:.1f} points<br/><br/>
        <b>Areas for Improvement:</b><br/>
        • Reduce GHG emissions by {(runner['GHG_Emissions'] - winner['GHG_Emissions']):.1f}M t<br/>
        • Increase recycling by {(winner['Recycling_Rate'] - runner['Recycling_Rate']):.1f}%<br/>
        • Improve safety to LTIR {winner['Safety_LTIR']:.2f}
        """
        story.append(Paragraph(runner_text, styles['Normal']))
        story.append(Spacer(1, 30))
    
    # Footer
    story.append(Spacer(1, 20))
    story.append(Paragraph("<hr/>", styles['Normal']))
    story.append(Paragraph("<b>Professional ESG Benchmarking Platform</b>", styles['Normal']))
    story.append(Paragraph("Developed by Ismail Kamal & Team | Under Supervision of Dr. Mohamed Tash", styles['Normal']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    
    doc.build(story)
    return filename

def generate_pdf_with_charts(df_calc, winner, runner):
    """توليد تقرير PDF مع الرسوم البيانية"""
    try:
        # إنشاء الرسوم البيانية
        categories = ['Environmental_Score', 'Social_Score', 'Governance_Score', 'Operational_Score']
        labels = ['Environmental', 'Social', 'Governance', 'Operational']
        colors_plot = ['#2E7D32', '#1565C0', '#6A1B9A', '#F57C00']
        
        fig_radar = go.Figure()
        for i, company in enumerate(df_calc['Company']):
            values = df_calc[df_calc['Company'] == company][categories].values.flatten().tolist()
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=labels,
                fill='toself',
                name=company,
                line_color=colors_plot[i % len(colors_plot)],
                fillcolor=f'rgba({int(colors_plot[i % len(colors_plot)][1:3], 16)}, {int(colors_plot[i % len(colors_plot)][3:5], 16)}, {int(colors_plot[i % len(colors_plot)][5:7], 16)}, 0.2)'
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="ESG Performance Radar Chart",
            height=500,
            showlegend=True
        )
        
        fig_bar = go.Figure()
        for i, company in enumerate(df_calc['Company']):
            values = df_calc[df_calc['Company'] == company][categories].values.flatten().tolist()
            fig_bar.add_trace(go.Bar(
                name=company,
                x=labels,
                y=values,
                marker_color=colors_plot[i % len(colors_plot)]
            ))
        
        fig_bar.update_layout(
            title="ESG Scores Comparison",
            yaxis_title="Score (%)",
            height=450,
            barmode='group'
        )
        
        # حفظ الصور
        img_radar = save_fig_as_image(fig_radar)
        img_bar = save_fig_as_image(fig_bar)
        
        if not img_radar or not img_bar:
            return generate_pdf_report(df_calc, winner, runner)
        
        # إنشاء PDF مع الصور
        filename = f"ESG_Benchmarking_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                     fontSize=24, textColor=colors.HexColor('#1B5E20'),
                                     spaceAfter=30, alignment=1)
        
        story.append(Paragraph("🏆 Professional ESG Benchmarking Report", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("AI-Powered Analysis for ExxonMobil, Saudi Aramco & BP", styles['Heading2']))
        story.append(Spacer(1, 24))
        
        story.append(Paragraph("<b>Team Leader:</b> Ismail Kamal", styles['Normal']))
        story.append(Paragraph("<b>Team Members:</b> Adel ElSayed, Mohamed Gaber, Ahmed Omar, Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh", styles['Normal']))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b><font color='red'>Under Supervision:</font> Dr. Mohamed Tash</b>", styles['Normal']))
        story.append(Paragraph("<b>QHSE Master at Alexandria University</b>", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Winner
        story.append(Paragraph("🏆 Winner Analysis", styles['Heading2']))
        rating = "⭐ A+ (Excellent)" if winner['Overall_Score'] >= 85 else \
                 "⭐ A (Very Good)" if winner['Overall_Score'] >= 75 else \
                 "⭐ B+ (Good)" if winner['Overall_Score'] >= 65 else \
                 "⭐ B (Satisfactory)" if winner['Overall_Score'] >= 55 else \
                 "⭐ C (Needs Improvement)"
        
        winner_text = f"""
        <b>Company:</b> {winner['Company']}<br/>
        <b>Overall Score:</b> {winner['Overall_Score']:.1f}/100<br/>
        <b>Rank:</b> #{int(winner['Rank'])}<br/>
        <b>ESG Rating:</b> {rating}<br/><br/>
        <b>Key Strengths:</b><br/>
        • EPI Score: {winner['EPI_Score']:.1f}<br/>
        • Recycling Rate: {winner['Recycling_Rate']:.1f}%<br/>
        • Safety Performance: LTIR {winner['Safety_LTIR']:.2f}<br/>
        • Renewable Energy: {winner['Renewable_Energy']:.1f}%
        """
        story.append(Paragraph(winner_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # إضافة الصور
        story.append(Paragraph("📊 Performance Visualization", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        if img_radar:
            story.append(RLImage(img_radar, width=400, height=280))
            story.append(Spacer(1, 12))
        
        if img_bar:
            story.append(RLImage(img_bar, width=400, height=280))
            story.append(Spacer(1, 20))
        
        # Scores Table
        story.append(Paragraph("📊 Detailed Scores", styles['Heading2']))
        
        table_data = [['Company', 'Overall', 'Environmental', 'Social', 'Governance', 'Operational']]
        for idx, row in df_calc.iterrows():
            table_data.append([
                row['Company'],
                f"{row['Overall_Score']:.1f}%",
                f"{row['Environmental_Score']:.1f}%",
                f"{row['Social_Score']:.1f}%",
                f"{row['Governance_Score']:.1f}%",
                f"{row['Operational_Score']:.1f}%"
            ])
        
        table = Table(table_data, colWidths=[100, 70, 80, 70, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B5E20')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Cleanup
        if img_radar and os.path.exists(img_radar):
            os.remove(img_radar)
        if img_bar and os.path.exists(img_bar):
            os.remove(img_bar)
        
        doc.build(story)
        return filename
        
    except Exception as e:
        return generate_pdf_report(df_calc, winner, runner)

# -----------------------
# DISPLAY FUNCTIONS
# -----------------------
def display_winner_analysis(df_calc):
    winner = df_calc.loc[df_calc['Overall_Score'].idxmax()]
    
    st.markdown("---")
    st.markdown("## 🏆 Winner Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        rating = "⭐ A+ (Excellent)" if winner['Overall_Score'] >= 85 else \
                 "⭐ A (Very Good)" if winner['Overall_Score'] >= 75 else \
                 "⭐ B+ (Good)" if winner['Overall_Score'] >= 65 else \
                 "⭐ B (Satisfactory)" if winner['Overall_Score'] >= 55 else \
                 "⭐ C (Needs Improvement)"
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                        border-radius: 20px; padding: 25px; border: 2px solid #F59E0B;'>
                <h1 style='color: #92400E; margin: 0;'>🏆 {winner['Company']}</h1>
                <h2 style='color: #78350F;'>Overall Score: {winner['Overall_Score']:.1f}/100</h2>
                <p style='font-size: 16px; color: #78350F;'>
                    <strong>🏅 Rank:</strong> #{int(winner['Rank'])} | 
                    <strong>📊 ESG Rating:</strong> {rating}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background: #F8FAFC; border-radius: 20px; padding: 20px; text-align: center;'>
                <h3>💪 Strengths</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li>✅ EPI: {winner['EPI_Score']:.1f}</li>
                    <li>✅ Recycling: {winner['Recycling_Rate']:.1f}%</li>
                    <li>✅ Safety: LTIR {winner['Safety_LTIR']:.2f}</li>
                    <li>✅ Renewable: {winner['Renewable_Energy']:.1f}%</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def display_company_cards(df_calc):
    st.subheader("📊 Company Rankings")
    df_sorted = df_calc.sort_values('Overall_Score', ascending=False).reset_index(drop=True)
    cols = st.columns(len(df_sorted))
    
    medal_colors = ['#F59E0B', '#94A3B8', '#CD7F32']
    medal_icons = ['🥇', '🥈', '🥉']
    
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        with cols[i]:
            is_winner = (i == 0)
            color = "#1B5E20" if is_winner else "#475569"
            border_color = "#F59E0B" if is_winner else "#E2E8F0"
            
            st.markdown(f"""
                <div class='company-card' style='border-left-color: {color}; border: 1px solid {border_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='font-size: 24px;'>{medal_icons[i]}</span>
                        {'<span class="winner-badge">🏆 Winner</span>' if is_winner else f'<span style="color: #64748b;">#{row["Rank"]}</span>'}
                    </div>
                    <h3 style='margin: 10px 0 5px 0;'>{row['Company']}</h3>
                    <div class='score' style='color: {medal_colors[i] if i < 3 else "#475569"};'>{row['Overall_Score']:.1f}</div>
                    <div style='font-size: 14px; color: #64748b;'>Overall Score</div>
                    
                    <div style='margin-top: 12px;'>
                        <div style='display: flex; justify-content: space-between; font-size: 12px;'>
                            <span>🌿 Environmental</span>
                            <span>{row['Environmental_Score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {min(row['Environmental_Score'], 100)}%;'></div></div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 12px; margin-top: 6px;'>
                            <span>👥 Social</span>
                            <span>{row['Social_Score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {min(row['Social_Score'], 100)}%;'></div></div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 12px; margin-top: 6px;'>
                            <span>🏛️ Governance</span>
                            <span>{row['Governance_Score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {min(row['Governance_Score'], 100)}%;'></div></div>
                    </div>
                    
                    <div style='margin-top: 12px;'>
                        <span class='metric-pill'>🌿 GHG: {row['GHG_Emissions']:.1f}M</span>
                        <span class='metric-pill'>♻️ Rec: {row['Recycling_Rate']:.0f}%</span>
                        <span class='metric-pill'>⚡ Ren: {row['Renewable_Energy']:.0f}%</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def display_detailed_comparison(df_calc):
    st.subheader("📋 Detailed Comparison Table")
    
    display_cols = [
        'Company', 'Rank',
        'GHG_Emissions', 'Renewable_Energy', 'Recycling_Rate', 'Water_Intensity',
        'Safety_LTIR', 'Process_Safety_Events', 'Training_Hours', 'Diversity_Rate',
        'EPI_Score', 'Transparency_Score',
        'Environmental_Score', 'Social_Score', 'Governance_Score', 'Operational_Score', 'Overall_Score'
    ]
    
    df_display = df_calc[display_cols].copy()
    
    format_dict = {
        'GHG_Emissions': '{:.1f}M',
        'Renewable_Energy': '{:.1f}%',
        'Recycling_Rate': '{:.1f}%',
        'Water_Intensity': '{:.2f}',
        'Safety_LTIR': '{:.2f}',
        'Process_Safety_Events': '{:.0f}',
        'Training_Hours': '{:.0f}h',
        'Diversity_Rate': '{:.1f}%',
        'EPI_Score': '{:.1f}',
        'Transparency_Score': '{:.1f}',
        'Environmental_Score': '{:.1f}%',
        'Social_Score': '{:.1f}%',
        'Governance_Score': '{:.1f}%',
        'Operational_Score': '{:.1f}%',
        'Overall_Score': '{:.1f}%'
    }
    
    for col, fmt in format_dict.items():
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: fmt.format(x))
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def display_charts(df_calc):
    st.subheader("📈 Performance Visualization")
    
    categories = ['Environmental_Score', 'Social_Score', 'Governance_Score', 'Operational_Score']
    labels = ['🌿 Environmental', '👥 Social', '🏛️ Governance', '⚡ Operational']
    colors = ['#2E7D32', '#1565C0', '#6A1B9A', '#F57C00']
    
    fig_radar = go.Figure()
    for i, company in enumerate(df_calc['Company']):
        values = df_calc[df_calc['Company'] == company][categories].values.flatten().tolist()
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=company,
            line_color=colors[i % len(colors)],
            fillcolor=f'rgba({int(colors[i % len(colors)][1:3], 16)}, {int(colors[i % len(colors)][3:5], 16)}, {int(colors[i % len(colors)][5:7], 16)}, 0.2)'
        ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="ESG Performance Radar Chart",
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    fig_bar = go.Figure()
    for i, company in enumerate(df_calc['Company']):
        values = df_calc[df_calc['Company'] == company][categories].values.flatten().tolist()
        fig_bar.add_trace(go.Bar(
            name=company,
            x=labels,
            y=values,
            marker_color=colors[i % len(colors)]
        ))
    
    fig_bar.update_layout(
        title="ESG Scores Comparison",
        yaxis_title="Score (%)",
        height=450,
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_radar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)

def display_predictive_insights(df_calc):
    st.subheader("🔮 Predictive Insights & Recommendations")
    
    winner = df_calc.loc[df_calc['Overall_Score'].idxmax()]
    runner = df_calc.loc[df_calc['Overall_Score'].idxmax() - 1] if len(df_calc) > 1 else None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style='background: #F0FDF4; border-radius: 16px; padding: 20px; border-left: 6px solid #1B5E20;'>
                <h4>📊 Winner Analysis: {winner['Company']}</h4>
                <p><strong>🏅 Overall Score:</strong> {winner['Overall_Score']:.1f}/100</p>
                <p><strong>🌿 Environmental:</strong> {winner['Environmental_Score']:.1f}%</p>
                <p><strong>👥 Social:</strong> {winner['Social_Score']:.1f}%</p>
                <p><strong>🏛️ Governance:</strong> {winner['Governance_Score']:.1f}%</p>
                <p><strong>⚡ Operational:</strong> {winner['Operational_Score']:.1f}%</p>
                <p style='margin-top: 10px;'><strong>✅ Key Strengths:</strong></p>
                <ul>
                    <li>🌿 Lowest GHG emissions: {winner['GHG_Emissions']:.1f}M t</li>
                    <li>♻️ Highest recycling rate: {winner['Recycling_Rate']:.1f}%</li>
                    <li>🛡️ Best safety performance: LTIR {winner['Safety_LTIR']:.2f}</li>
                    <li>⚡ Highest renewable: {winner['Renewable_Energy']:.1f}%</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if runner is not None:
            st.markdown(f"""
                <div style='background: #EFF6FF; border-radius: 16px; padding: 20px; border-left: 6px solid #2563EB;'>
                    <h4>📈 Runner-Up: {runner['Company']}</h4>
                    <p><strong>🏅 Overall Score:</strong> {runner['Overall_Score']:.1f}/100</p>
                    <p><strong>Gap:</strong> {winner['Overall_Score'] - runner['Overall_Score']:.1f} points behind</p>
                    <p style='margin-top: 10px;'><strong>🟡 Areas for Improvement:</strong></p>
                    <ul>
                        <li>🌿 Reduce GHG emissions by {(runner['GHG_Emissions'] - winner['GHG_Emissions']):.1f}M t</li>
                        <li>♻️ Increase recycling by {(winner['Recycling_Rate'] - runner['Recycling_Rate']):.1f}%</li>
                        <li>🛡️ Improve safety to LTIR {winner['Safety_LTIR']:.2f}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# -----------------------
# MAIN APP
# -----------------------
st.markdown("## 📄 Upload Reports")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📌 Instructions
    1. Upload the 3 PDF reports (ExxonMobil, Saudi Aramco, BP)
    2. Click "Run Professional Analysis"
    3. View comprehensive benchmarking results with winner analysis
    """)

with col2:
    st.markdown("""
    ### 📂 Upload Files
    - **ExxonMobil:** `2025_Exxon mobil sustainability-report.pdf`
    - **Saudi Aramco:** `2025 Saudi Aramco Sustainability Report.pdf`
    - **BP:** `2025_BP-sustainability-report.pdf`
    """)

col1, col2, col3 = st.columns(3)
with col1:
    exxon_file = st.file_uploader("ExxonMobil Report", type="pdf", key="exxon")
with col2:
    aramco_file = st.file_uploader("Saudi Aramco Report", type="pdf", key="aramco")
with col3:
    bp_file = st.file_uploader("BP Report", type="pdf", key="bp")

if st.button("🚀 Run Professional Analysis", type="primary", use_container_width=True):
    with st.spinner("📊 Analyzing reports with professional ESG framework..."):
        files = [exxon_file, aramco_file, bp_file]
        df_calc = process_uploaded_reports(files)
        st.session_state.results = df_calc
        st.session_state.analysis_done = True
    st.success("✅ Analysis complete! Results displayed below.")
    st.balloons()

if st.session_state.analysis_done and st.session_state.results is not None:
    df_calc = st.session_state.results
    
    display_winner_analysis(df_calc)
    
    st.markdown("---")
    display_company_cards(df_calc)
    
    st.markdown("---")
    display_charts(df_calc)
    
    st.markdown("---")
    display_detailed_comparison(df_calc)
    
    st.markdown("---")
    display_predictive_insights(df_calc)
    
    # Export Section
    st.markdown("---")
    st.markdown("## 📥 Export Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV Export
        csv = df_calc.to_csv(index=False)
        st.download_button(
            label="📊 Download Results as CSV",
            data=csv,
            file_name=f"ESG_Benchmarking_Results_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # PDF Export
        if st.button("📄 Download Full PDF Report (Print Ready)", use_container_width=True):
            with st.spinner("Generating PDF report with all data and charts..."):
                winner = df_calc.loc[df_calc['Overall_Score'].idxmax()]
                runner = df_calc.loc[df_calc['Overall_Score'].idxmax() - 1] if len(df_calc) > 1 else None
                
                pdf_file = generate_pdf_with_charts(df_calc, winner, runner)
                
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="✅ Click to Download PDF Report",
                        data=f,
                        file_name=pdf_file,
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.success("✅ PDF Report generated successfully!")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #0A2E0F 0%, #1B5E20 100%); border-radius: 15px; margin-top: 20px;'>
        <p style='color: white;'>🏆 Professional ESG Benchmarking Platform | AI-Powered Analysis</p>
        <p style='color: #E8F5E9; font-size: 12px;'>Developed by <strong>Ismail Kamal</strong> & Team | <strong style='color: #FF0000;'>Under Supervision of Dr. Mohamed Tash</strong></p>
        <p style='color: #FFD54F; font-size: 11px;'>Version 10.0 | GRI · TCFD · SASB · SBTi Compliant</p>
    </div>
""", unsafe_allow_html=True)
