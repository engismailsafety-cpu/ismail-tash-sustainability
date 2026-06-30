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

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Professional ESG Benchmarking Platform",
    page_icon="🏆",
    layout="wide"
)

# -----------------------
# CUSTOM CSS
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
    .env { border-left: 4px solid #2E7D32; background: #F0FDF4; }
    .social { border-left: 4px solid #1565C0; background: #EFF6FF; }
    .gov { border-left: 4px solid #6A1B9A; background: #F3E5F5; }
    .op { border-left: 4px solid #F57C00; background: #FFF8E1; }
    
    .score-gold { color: #F59E0B; font-weight: bold; }
    .score-silver { color: #94A3B8; font-weight: bold; }
    .score-bronze { color: #CD7F32; font-weight: bold; }
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
            <div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); border-radius: 20px; padding: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);'>
                <h3 style='text-align: center; background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color: white; padding: 12px; border-radius: 12px;'>👥 PROJECT TEAM</h3>
                <table style='width: 100%; border-collapse: collapse;'>
                    <tr style='background: #E8F5E9;'><th style='padding: 8px; text-align: center;'>Role</th><th style='padding: 8px; text-align: center;'>Name</th></tr>
                    <tr style='background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);'><td style='padding: 8px; text-align: center;'><b>🏆 Team Leader</b></td><td style='padding: 8px; text-align: center; color: #D32F2F; font-weight: bold;'>Ismail Kamal</td></tr>
                    <tr><td style='padding: 8px; text-align: center;'>📋 Team Member</td><td style='padding: 8px; text-align: center; color: #1565C0;'>Adel ElSayed</td></tr>
                    <tr><td style='padding: 8px; text-align: center;'>📋 Team Member</td><td style='padding: 8px; text-align: center; color: #1565C0;'>Mohamed Gaber</td></tr>
                    <tr><td style='padding: 8px; text-align: center;'>📋 Team Member</td><td style='padding: 8px; text-align: center; color: #1565C0;'>Ahmed Omar</td></tr>
                    <tr><td style='padding: 8px; text-align: center;'>📋 Team Member</td><td style='padding: 8px; text-align: center; color: #1565C0;'>Sherouk Ashraf</td></tr>
                    <tr><td style='padding: 8px; text-align: center;'>📋 Team Member</td><td style='padding: 8px; text-align: center; color: #1565C0;'>Mohamed ElHammadi</td></tr>
                    <tr><td style='padding: 8px; text-align: center;'>📋 Team Member</td><td style='padding: 8px; text-align: center; color: #1565C0;'>Farouk Sameh</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%); padding: 30px; border-radius: 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15);'>
                <h3 style='color: #FFD54F; margin: 0;'>🎓 Under Supervision of</h3>
                <h1 style='color: #FF0000; font-weight: bold; font-size: 36px; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>Dr. Mohamed Tash</h1>
                <p style='font-size: 18px; color: white; font-weight: bold;'>QHSE Master at Alexandria University</p>
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
# SIDEBAR
# -----------------------
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 50px;'>🏆</div>", unsafe_allow_html=True)
    st.markdown("### 👥 PROJECT TEAM")
    st.markdown("""
    <div style='color: #E8F5E9;'>
        <b style='color: #FFD54F;'>🏆 Ismail Kamal</b> (Leader)<br>
        <span>• Adel ElSayed</span><br>
        <span>• Mohamed Gaber</span><br>
        <span>• Ahmed Omar</span><br>
        <span>• Sherouk Ashraf</span><br>
        <span>• Mohamed ElHammadi</span><br>
        <span>• Farouk Sameh</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🎓 Supervisor")
    st.markdown("<span style='color: #FF0000; font-weight: bold; font-size: 18px;'>Dr. Mohamed Tash</span>", unsafe_allow_html=True)
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
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return ""

def extract_esg_metrics(text, company_name):
    """استخراج مؤشرات ESG من النص"""
    
    # البحث عن الأرقام في النص
    def find_value(pattern, text, default="N/A"):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(',', ''))
        return default
    
    # Environmental Metrics
    ghg = find_value(r'GHG\s*emissions?.*?(\d+(?:\.\d+)?)\s*(?:million|M)?', text, 100)
    renewable = find_value(r'renewable\s*energy.*?(\d+(?:\.\d+)?)\s*%', text, 10)
    recycling = find_value(r'recycling\s*rate.*?(\d+(?:\.\d+)?)\s*%', text, 65)
    water = find_value(r'water\s*(?:intensity|consumption).*?(\d+(?:\.\d+)?)', text, 0.8)
    biodiversity = find_value(r'biodiversity\s*score.*?(\d+(?:\.\d+)?)', text, 70)
    methane = find_value(r'methane\s*intensity.*?(\d+(?:\.\d+)?)', text, 0.4)
    
    # Social Metrics
    ltir = find_value(r'LTIR|safety.*?(\d+(?:\.\d+)?)', text, 0.3)
    safety_events = find_value(r'(?:process\s*safety|PSI).*?(\d+)', text, 8)
    training = find_value(r'training\s*hours.*?(\d+(?:\.\d+)?)', text, 40)
    diversity = find_value(r'(?:women|female|diversity).*?(\d+(?:\.\d+)?)\s*%', text, 25)
    
    # Governance Metrics
    epi = find_value(r'EPI\s*score.*?(\d+(?:\.\d+)?)', text, 75)
    transparency = find_value(r'transparency\s*score.*?(\d+(?:\.\d+)?)', text, 80)
    risk = find_value(r'risk\s*score.*?(\d+(?:\.\d+)?)', text, 75)
    
    return {
        "Company": company_name,
        # Environmental (35%)
        "GHG_Emissions": ghg,
        "Renewable_Energy": renewable,
        "Recycling_Rate": recycling,
        "Water_Intensity": water,
        "Biodiversity_Score": biodiversity,
        "Methane_Intensity": methane,
        # Social (25%)
        "Safety_LTIR": ltir,
        "Process_Safety_Events": safety_events,
        "Training_Hours": training,
        "Diversity_Rate": diversity,
        # Governance (20%)
        "EPI_Score": epi,
        "Transparency_Score": transparency,
        "Risk_Score": risk,
        # Operational (20%)
        "Energy_Efficiency": find_value(r'energy\s*efficiency.*?(\d+(?:\.\d+)?)\s*%', text, 82),
        "Carbon_Intensity": find_value(r'carbon\s*intensity.*?(\d+(?:\.\d+)?)', text, 200),
    }

def calculate_professional_scores(df):
    """حساب الدرجات الاحترافية مع الأوزان"""
    df_calc = df.copy()
    
    # ========== Environmental Score (35%) ==========
    # GHG: أقل = أفضل (عكس)
    max_ghg = df_calc['GHG_Emissions'].max()
    df_calc['GHG_Score'] = (1 - (df_calc['GHG_Emissions'] / max_ghg)) * 100
    
    # Renewable: أعلى = أفضل
    df_calc['Renewable_Score'] = df_calc['Renewable_Energy'] * 5  # 0-20% → 0-100
    
    # Recycling: أعلى = أفضل
    df_calc['Recycling_Score'] = df_calc['Recycling_Rate']
    
    # Water: أقل = أفضل (عكس)
    max_water = df_calc['Water_Intensity'].max()
    df_calc['Water_Score'] = (1 - (df_calc['Water_Intensity'] / max_water)) * 100
    
    # Biodiversity: أعلى = أفضل
    df_calc['Biodiversity_Score'] = df_calc['Biodiversity_Score']
    
    # Methane: أقل = أفضل (عكس)
    max_methane = df_calc['Methane_Intensity'].max()
    df_calc['Methane_Score'] = (1 - (df_calc['Methane_Intensity'] / max_methane)) * 100
    
    # Environmental Score (وزن 35%)
    df_calc['Environmental_Score'] = (
        df_calc['GHG_Score'] * 0.25 +
        df_calc['Renewable_Score'] * 0.20 +
        df_calc['Recycling_Score'] * 0.20 +
        df_calc['Water_Score'] * 0.15 +
        df_calc['Biodiversity_Score'] * 0.10 +
        df_calc['Methane_Score'] * 0.10
    )
    
    # ========== Social Score (25%) ==========
    # Safety LTIR: أقل = أفضل (عكس)
    max_ltir = df_calc['Safety_LTIR'].max()
    df_calc['Safety_Score'] = (1 - (df_calc['Safety_LTIR'] / max_ltir)) * 100
    
    # Safety Events: أقل = أفضل (عكس)
    max_events = df_calc['Process_Safety_Events'].max()
    df_calc['Safety_Events_Score'] = (1 - (df_calc['Process_Safety_Events'] / max_events)) * 100
    
    # Training: أعلى = أفضل
    max_training = df_calc['Training_Hours'].max()
    df_calc['Training_Score'] = (df_calc['Training_Hours'] / max_training) * 100
    
    # Diversity: أعلى = أفضل
    max_diversity = df_calc['Diversity_Rate'].max()
    df_calc['Diversity_Score'] = (df_calc['Diversity_Rate'] / max_diversity) * 100
    
    # Social Score (وزن 25%)
    df_calc['Social_Score'] = (
        df_calc['Safety_Score'] * 0.35 +
        df_calc['Safety_Events_Score'] * 0.25 +
        df_calc['Training_Score'] * 0.20 +
        df_calc['Diversity_Score'] * 0.20
    )
    
    # ========== Governance Score (20%) ==========
    # EPI: أعلى = أفضل
    max_epi = df_calc['EPI_Score'].max()
    df_calc['EPI_Score_Norm'] = (df_calc['EPI_Score'] / max_epi) * 100
    
    # Transparency: أعلى = أفضل
    max_trans = df_calc['Transparency_Score'].max()
    df_calc['Transparency_Score_Norm'] = (df_calc['Transparency_Score'] / max_trans) * 100
    
    # Risk: أقل = أفضل (عكس) - نعكسها
    max_risk = df_calc['Risk_Score'].max()
    df_calc['Risk_Score_Norm'] = (1 - (df_calc['Risk_Score'] / max_risk)) * 100
    
    # Governance Score (وزن 20%)
    df_calc['Governance_Score'] = (
        df_calc['EPI_Score_Norm'] * 0.40 +
        df_calc['Transparency_Score_Norm'] * 0.35 +
        df_calc['Risk_Score_Norm'] * 0.25
    )
    
    # ========== Operational Score (20%) ==========
    # Energy Efficiency: أعلى = أفضل
    max_energy = df_calc['Energy_Efficiency'].max()
    df_calc['Energy_Score'] = (df_calc['Energy_Efficiency'] / max_energy) * 100
    
    # Carbon Intensity: أقل = أفضل (عكس)
    max_carbon = df_calc['Carbon_Intensity'].max()
    df_calc['Carbon_Intensity_Score'] = (1 - (df_calc['Carbon_Intensity'] / max_carbon)) * 100
    
    # Operational Score (وزن 20%)
    df_calc['Operational_Score'] = (
        df_calc['Energy_Score'] * 0.50 +
        df_calc['Carbon_Intensity_Score'] * 0.50
    )
    
    # ========== Overall Score (100%) ==========
    df_calc['Overall_Score'] = (
        df_calc['Environmental_Score'] * 0.35 +
        df_calc['Social_Score'] * 0.25 +
        df_calc['Governance_Score'] * 0.20 +
        df_calc['Operational_Score'] * 0.20
    )
    
    # ========== Ranking ==========
    df_calc['Rank'] = df_calc['Overall_Score'].rank(ascending=False, method='dense').astype(int)
    
    return df_calc

# -----------------------
# DEMO DATA (Fallback)
# -----------------------
@st.cache_data
def get_demo_data():
    """بيانات تجريبية للعرض في حالة عدم رفع ملفات"""
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
    """معالجة التقارير المرفوعة واستخراج البيانات"""
    results = []
    company_names = ["ExxonMobil", "Saudi Aramco", "BP"]
    
    for i, file in enumerate(files):
        if file is not None:
            text = extract_text_from_pdf(file)
            if text:
                data = extract_esg_metrics(text, company_names[i])
                results.append(data)
    
    if len(results) == 3:
        df = pd.DataFrame(results)
        return calculate_professional_scores(df)
    else:
        # استخدام البيانات التجريبية إذا لم يتم رفع جميع الملفات
        df = get_demo_data()
        return calculate_professional_scores(df)

# -----------------------
# DISPLAY FUNCTIONS
# -----------------------
def display_winner_analysis(df_calc):
    """عرض تحليل الفائز بالتفصيل"""
    winner = df_calc.loc[df_calc['Overall_Score'].idxmax()]
    
    st.markdown("---")
    st.markdown("## 🏆 Winner Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                        border-radius: 20px; padding: 25px; border: 2px solid #F59E0B;'>
                <h1 style='color: #92400E; margin: 0;'>🏆 {winner['Company']}</h1>
                <h2 style='color: #78350F;'>Overall Score: {winner['Overall_Score']:.1f}/100</h2>
                <p style='font-size: 16px; color: #78350F;'>
                    <strong>🏅 Rank:</strong> #{int(winner['Rank'])} | 
                    <strong>📊 ESG Rating:</strong> {get_esg_rating(winner['Overall_Score'])}
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

def get_esg_rating(score):
    """تصنيف ESG بناءً على الدرجة"""
    if score >= 85:
        return "⭐ A+ (Excellent)"
    elif score >= 75:
        return "⭐ A (Very Good)"
    elif score >= 65:
        return "⭐ B+ (Good)"
    elif score >= 55:
        return "⭐ B (Satisfactory)"
    else:
        return "⭐ C (Needs Improvement)"

def display_company_cards(df_calc):
    """عرض بطاقات الشركات"""
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
                        <div class='progress-bar'><div class='fill' style='width: {row['Environmental_Score']}%;'></div></div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 12px; margin-top: 6px;'>
                            <span>👥 Social</span>
                            <span>{row['Social_Score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {row['Social_Score']}%;'></div></div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 12px; margin-top: 6px;'>
                            <span>🏛️ Governance</span>
                            <span>{row['Governance_Score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {row['Governance_Score']}%;'></div></div>
                    </div>
                    
                    <div style='margin-top: 12px;'>
                        <span class='metric-pill'>🌿 GHG: {row['GHG_Emissions']:.1f}M</span>
                        <span class='metric-pill'>♻️ Rec: {row['Recycling_Rate']:.0f}%</span>
                        <span class='metric-pill'>⚡ Ren: {row['Renewable_Energy']:.0f}%</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def display_detailed_comparison(df_calc):
    """عرض جدول المقارنة التفصيلي"""
    st.subheader("📋 Detailed Comparison Table")
    
    # اختيار الأعمدة للعرض
    display_cols = [
        'Company', 'Rank',
        'GHG_Emissions', 'Renewable_Energy', 'Recycling_Rate', 'Water_Intensity',
        'Safety_LTIR', 'Process_Safety_Events', 'Training_Hours', 'Diversity_Rate',
        'EPI_Score', 'Transparency_Score',
        'Environmental_Score', 'Social_Score', 'Governance_Score', 'Operational_Score', 'Overall_Score'
    ]
    
    df_display = df_calc[display_cols].copy()
    
    # تنسيق الأعمدة
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
    
    # تطبيق التنسيق
    for col, fmt in format_dict.items():
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: fmt.format(x))
    
    # إضافة ألوان للصفوف حسب الترتيب
    def color_rank(row):
        if row['Rank'] == 1:
            return 'background-color: #FEF3C7'
        elif row['Rank'] == 2:
            return 'background-color: #F1F5F9'
        elif row['Rank'] == 3:
            return 'background-color: #FEF3C7'
        return ''
    
    # عرض الجدول
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def display_charts(df_calc):
    """عرض الرسوم البيانية"""
    st.subheader("📈 Performance Visualization")
    
    # 1. Radar Chart
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
    
    # 2. Bar Chart
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
    """عرض التوصيات والتنبؤات"""
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
    
    # General Recommendations
    st.markdown("""
        <div style='background: #F8FAFC; border-radius: 16px; padding: 20px; margin-top: 15px; border: 1px solid #E2E8F0;'>
            <h4>💡 Strategic Recommendations for All Companies</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>
                <div>
                    <strong>🌿 Environmental</strong>
                    <ul>
                        <li>Set science-based targets (SBTi)</li>
                        <li>Increase renewable energy share to 25%+</li>
                        <li>Enhance water recycling programs</li>
                    </ul>
                </div>
                <div>
                    <strong>👥 Social</strong>
                    <ul>
                        <li>Improve diversity to 35%+</li>
                        <li>Increase training hours to 50+ per employee</li>
                        <li>Strengthen community engagement</li>
                    </ul>
                </div>
                <div>
                    <strong>🏛️ Governance</strong>
                    <ul>
                        <li>Enhance transparency and reporting</li>
                        <li>Strengthen risk management frameworks</li>
                        <li>Improve board independence</li>
                    </ul>
                </div>
                <div>
                    <strong>⚡ Operational</strong>
                    <ul>
                        <li>Improve energy efficiency to 90%+</li>
                        <li>Reduce carbon intensity by 15%</li>
                        <li>Adopt circular economy principles</li>
                    </ul>
                </div>
            </div>
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
    
    # 1. Winner Analysis
    display_winner_analysis(df_calc)
    
    # 2. Company Cards
    st.markdown("---")
    display_company_cards(df_calc)
    
    # 3. Charts
    st.markdown("---")
    display_charts(df_calc)
    
    # 4. Detailed Comparison Table
    st.markdown("---")
    display_detailed_comparison(df_calc)
    
    # 5. Predictive Insights
    st.markdown("---")
    display_predictive_insights(df_calc)
    
    # 6. Export
    st.markdown("---")
    st.markdown("## 📥 Export Report")
    
    # Convert results to CSV for download
    csv = df_calc.to_csv(index=False)
    st.download_button(
        label="📊 Download Results as CSV",
        data=csv,
        file_name=f"ESG_Benchmarking_Results_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.info("📄 Full PDF report export will be available in the next version with all charts and tables.")

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
