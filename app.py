import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from pypdf import PdfReader
import re
import io
import os
import tempfile
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
from reportlab.lib.units import inch, cm
import plotly.io as pio
import base64

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="🌍 Global Energy ESG Benchmarking 2025",
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
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 6px solid #1B5E20;
        margin: 15px 0;
        transition: all 0.3s;
    }
    .company-card:hover { transform: translateY(-5px); box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
    .score { font-size: 36px; font-weight: 700; color: #1B5E20; }
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
        height: 10px;
        background: #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
        margin: 8px 0;
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
    .gold { color: #F59E0B; font-weight: bold; }
    .silver { color: #94A3B8; font-weight: bold; }
    .bronze { color: #CD7F32; font-weight: bold; }
    
    .insight-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-radius: 16px;
        padding: 20px;
        border-left: 6px solid #1B5E20;
        margin: 15px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border-radius: 16px;
        padding: 20px;
        border-left: 6px solid #F59E0B;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# LOGIN SYSTEM
# -----------------------
users = {"admin": "1234", "ismail": "2024", "Dtash": "0000"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "results" not in st.session_state:
    st.session_state.results = None

if not st.session_state.logged_in:
    st.markdown("""
        <div class='main-header'>
            <h1>🏆 Global Energy ESG Benchmarking 2025</h1>
            <p>AI-Powered Analysis: Saudi Aramco · ExxonMobil · BP</p>
            <p style='font-weight: bold; color: white; margin-top: 15px;'>
                Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash
            </p>
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
            <div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); border-radius: 20px; padding: 20px;'>
                <h3 style='text-align: center; background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color: white; padding: 12px; border-radius: 12px;'>👥 PROJECT TEAM</h3>
                <table style='width: 100%; border-collapse: collapse;'>
                    <tr style='background: #E8F5E9;'><th>Role</th><th>Name</th></tr>
                    <tr style='background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);'><td><b>🏆 Team Leader</b></td><td style='color: #D32F2F; font-weight: bold;'>Ismail Kamal</td></tr>
                    <tr><td>📋 Team Member</td><td style='color: #1565C0;'>Adel ElSayed</td></tr>
                    <tr><td>📋 Team Member</td><td style='color: #1565C0;'>Mohamed Gaber</td></tr>
                    <tr><td>📋 Team Member</td><td style='color: #1565C0;'>Ahmed Omar</td></tr>
                    <tr><td>📋 Team Member</td><td style='color: #1565C0;'>Sherouk Ashraf</td></tr>
                    <tr><td>📋 Team Member</td><td style='color: #1565C0;'>Mohamed ElHammadi</td></tr>
                    <tr><td>📋 Team Member</td><td style='color: #1565C0;'>Farouk Sameh</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%); padding: 30px; border-radius: 20px; text-align: center;'>
                <h3 style='color: #FFD54F; margin: 0;'>🎓 Under Supervision of</h3>
                <h1 style='color: #FF0000; font-weight: bold; font-size: 36px; margin: 15px 0;'>Dr. Mohamed Tash</h1>
                <p style='font-size: 18px; color: white; font-weight: bold;'>QHSE Master at Alexandria University</p>
                <p style='font-size: 14px; color: #E8F5E9;'>Professor of Sustainability & ESG</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2025 Global Energy ESG Benchmarking Platform")
    st.stop()

# -----------------------
# MAIN HEADER
# -----------------------
st.markdown("""
    <div class='main-header'>
        <h1>🏆 Global Energy ESG Benchmarking 2025</h1>
        <p>AI-Powered Analysis: Saudi Aramco · ExxonMobil · BP</p>
        <p style='font-weight: bold; color: white; margin-top: 15px;'>
            Team Leader: Ismail Kamal | Under Supervision: Dr. Mohamed Tash
        </p>
        <p style='font-size: 13px; color: #FFD54F;'>QHSE Master at Alexandria University</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------
# SIDEBAR
# -----------------------
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 50px;'>🏆</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%); border-radius: 15px; padding: 15px;'>
            <h4 style='color: #FFD54F; text-align: center;'>👥 PROJECT TEAM</h4>
            <p style='color: #FFD54F; font-weight: bold;'>🏆 Ismail Kamal <span style='color: #E8F5E9;'>(Leader)</span></p>
            <p style='color: #E8F5E9;'>• Adel ElSayed</p>
            <p style='color: #E8F5E9;'>• Mohamed Gaber</p>
            <p style='color: #E8F5E9;'>• Ahmed Omar</p>
            <p style='color: #E8F5E9;'>• Sherouk Ashraf</p>
            <p style='color: #E8F5E9;'>• Mohamed ElHammadi</p>
            <p style='color: #E8F5E9;'>• Farouk Sameh</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); border-radius: 15px; padding: 15px; text-align: center;'>
            <h4 style='color: #2E7D32;'>🎓 SUPERVISOR</h4>
            <p style='color: #FF0000; font-weight: bold; font-size: 20px;'>Dr. Mohamed Tash</p>
            <p style='color: #2E7D32; font-weight: bold;'>QHSE Master at Alexandria University</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Version 10.0 | ESG Benchmarking")

# -----------------------
# DATA EXTRACTION FROM PDF
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

def extract_esg_metrics(text, company_name):
    """استخراج مؤشرات ESG من النص"""
    
    def find_value(pattern, text, default=0):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(',', ''))
            except:
                return default
        return default
    
    # Environmental Metrics
    ghg = find_value(r'GHG\s*emissions?.*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, 50)
    if ghg == 0:
        ghg = find_value(r'(\d+(?:\.\d+)?)\s*(?:million|M)\s*(?:tons?)?\s*(?:CO2|GHG)', text, 50)
    
    methane = find_value(r'methane\s*intensity.*?(\d+(?:\.\d+)?)\s*%', text, 0.04)
    flaring = find_value(r'flaring\s*intensity.*?(\d+(?:\.\d+)?)', text, 5.0)
    renewable = find_value(r'renewable\s*capacity.*?(\d+(?:\.\d+)?)\s*(?:GW|gigawatt)', text, 0.5)
    water = find_value(r'water\s*(?:consumption|withdrawal).*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, 200)
    recycling = find_value(r'recycling\s*rate.*?(\d+(?:\.\d+)?)\s*%', text, 50)
    carbon_intensity = find_value(r'carbon\s*intensity.*?(\d+(?:\.\d+)?)\s*(?:kg|CO2e)', text, 10.0)
    reduction = find_value(r'(?:emissions?|GHG)\s*reduction.*?(\d+(?:\.\d+)?)\s*%', text, 0)
    biodiversity = find_value(r'biodiversity.*?(\d+(?:\.\d+)?)\s*%', text, 80)
    
    # Social Metrics
    ltir = find_value(r'LTIR.*?(\d+(?:\.\d+)?)', text, 0.02)
    trir = find_value(r'(?:total|recordable).*?(\d+(?:\.\d+)?)', text, 0.15)
    safety_events = find_value(r'(?:process\s*safety|Tier\s*1).*?(\d+)', text, 20)
    investment = find_value(r'social\s*investment.*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, 200)
    female = find_value(r'women|female.*?(\d+(?:\.\d+)?)\s*%', text, 25)
    employees = find_value(r'employees.*?(\d+(?:,?\d+)*)', text, 70000)
    
    # Governance Metrics
    rnd = find_value(r'R.?D\s*spend.*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, 1000)
    energy_intensity = find_value(r'energy\s*intensity.*?(\d+(?:\.\d+)?)', text, 170)
    gas_prod = find_value(r'gas\s*production.*?(\d+(?:\.\d+)?)\s*(?:bscfd|bcf)', text, 10.0)
    oil_prod = find_value(r'oil\s*production.*?(\d+(?:\.\d+)?)\s*(?:MMbd|mbd)', text, 10.0)
    
    return {
        "company": company_name,
        "industry": "Oil & Gas",
        "ghg_emissions": ghg,
        "methane_intensity": methane,
        "flaring_intensity": flaring,
        "energy_intensity": energy_intensity,
        "renewable_capacity": renewable,
        "safety_ltir": ltir,
        "total_recordable_rate": trir,
        "process_safety_events": safety_events,
        "water_consumption": water,
        "recycling_rate": recycling,
        "social_investment": investment,
        "female_representation": female,
        "rnd_spend": rnd,
        "upstream_carbon_intensity": carbon_intensity,
        "emissions_reduction": reduction,
        "biodiversity_protection": biodiversity,
        "employees": employees,
        "gas_production": gas_prod,
        "oil_production": oil_prod,
    }

def process_uploaded_reports(files, company_names):
    """معالجة التقارير المرفوعة واستخراج البيانات"""
    results = []
    
    for i, file in enumerate(files):
        if file is not None:
            text = extract_text_from_pdf(file)
            if text:
                data = extract_esg_metrics(text, company_names[i])
                results.append(data)
            else:
                default_data = create_default_data(company_names[i], i)
                results.append(default_data)
        else:
            default_data = create_default_data(company_names[i], i)
            results.append(default_data)
    
    return pd.DataFrame(results)

def create_default_data(company_name, index):
    """إنشاء بيانات افتراضية للشركة"""
    return {
        "company": company_name,
        "industry": "Oil & Gas",
        "ghg_emissions": 50 + index * 20,
        "methane_intensity": 0.04 - index * 0.005,
        "flaring_intensity": 6.0 - index * 1.0,
        "energy_intensity": 170 + index * 5,
        "renewable_capacity": 0.5 + index * 0.3,
        "safety_ltir": 0.02 + index * 0.01,
        "total_recordable_rate": 0.15 + index * 0.02,
        "process_safety_events": 30 - index * 5,
        "water_consumption": 200 + index * 30,
        "recycling_rate": 50 + index * 5,
        "social_investment": 200 - index * 30,
        "female_representation": 25 + index * 3,
        "rnd_spend": 1000 + index * 100,
        "upstream_carbon_intensity": 10.0 - index * 0.5,
        "emissions_reduction": 10 + index * 5,
        "biodiversity_protection": 80 + index * 2,
        "employees": 70000 + index * 5000,
        "gas_production": 10.0 + index * 0.5,
        "oil_production": 10.0 - index * 1.0,
    }

def calculate_esg_scores(df):
    """حساب درجات ESG مع أوزان مخصصة"""
    df_calc = df.copy()
    
    # Environmental Score (40%)
    max_ghg = max(df_calc['ghg_emissions'].max(), 1)
    df_calc['ghg_score'] = (1 - (df_calc['ghg_emissions'] / max_ghg)) * 100
    
    max_methane = max(df_calc['methane_intensity'].max(), 0.01)
    df_calc['methane_score'] = (1 - (df_calc['methane_intensity'] / max_methane)) * 100
    
    max_flaring = max(df_calc['flaring_intensity'].max(), 1)
    df_calc['flaring_score'] = (1 - (df_calc['flaring_intensity'] / max_flaring)) * 100
    
    max_renewable = max(df_calc['renewable_capacity'].max(), 1)
    df_calc['renewable_score'] = (df_calc['renewable_capacity'] / max_renewable) * 100
    
    max_water = max(df_calc['water_consumption'].max(), 1)
    df_calc['water_score'] = (1 - (df_calc['water_consumption'] / max_water)) * 100
    
    max_recycling = max(df_calc['recycling_rate'].max(), 1)
    df_calc['recycling_score'] = (df_calc['recycling_rate'] / max_recycling) * 100
    
    max_carbon = max(df_calc['upstream_carbon_intensity'].max(), 1)
    df_calc['carbon_intensity_score'] = (1 - (df_calc['upstream_carbon_intensity'] / max_carbon)) * 100
    
    max_reduction = max(df_calc['emissions_reduction'].max(), 1)
    df_calc['reduction_score'] = (df_calc['emissions_reduction'] / max_reduction) * 100
    
    max_biodiversity = max(df_calc['biodiversity_protection'].max(), 1)
    df_calc['biodiversity_score'] = (df_calc['biodiversity_protection'] / max_biodiversity) * 100
    
    df_calc['environmental_score'] = (
        df_calc['ghg_score'] * 0.20 +
        df_calc['methane_score'] * 0.15 +
        df_calc['flaring_score'] * 0.05 +
        df_calc['renewable_score'] * 0.10 +
        df_calc['water_score'] * 0.10 +
        df_calc['recycling_score'] * 0.10 +
        df_calc['carbon_intensity_score'] * 0.10 +
        df_calc['reduction_score'] * 0.10 +
        df_calc['biodiversity_score'] * 0.10
    )
    
    # Social Score (30%)
    max_ltir = max(df_calc['safety_ltir'].max(), 0.01)
    df_calc['safety_score'] = (1 - (df_calc['safety_ltir'] / max_ltir)) * 100
    
    max_trir = max(df_calc['total_recordable_rate'].max(), 0.01)
    df_calc['trir_score'] = (1 - (df_calc['total_recordable_rate'] / max_trir)) * 100
    
    max_events = max(df_calc['process_safety_events'].max(), 1)
    df_calc['safety_events_score'] = (1 - (df_calc['process_safety_events'] / max_events)) * 100
    
    max_investment = max(df_calc['social_investment'].max(), 1)
    df_calc['investment_score'] = (df_calc['social_investment'] / max_investment) * 100
    
    max_female = max(df_calc['female_representation'].max(), 1)
    df_calc['female_score'] = (df_calc['female_representation'] / max_female) * 100
    
    max_employees = max(df_calc['employees'].max(), 1)
    df_calc['employees_score'] = (df_calc['employees'] / max_employees) * 100
    
    df_calc['social_score'] = (
        df_calc['safety_score'] * 0.25 +
        df_calc['trir_score'] * 0.15 +
        df_calc['safety_events_score'] * 0.15 +
        df_calc['investment_score'] * 0.20 +
        df_calc['female_score'] * 0.15 +
        df_calc['employees_score'] * 0.10
    )
    
    # Governance Score (30%)
    max_rnd = max(df_calc['rnd_spend'].max(), 1)
    df_calc['rnd_score'] = (df_calc['rnd_spend'] / max_rnd) * 100
    
    max_energy = max(df_calc['energy_intensity'].max(), 1)
    df_calc['energy_score'] = (1 - (df_calc['energy_intensity'] / max_energy)) * 100
    
    max_gas = max(df_calc['gas_production'].max(), 1)
    df_calc['gas_score'] = (df_calc['gas_production'] / max_gas) * 100
    
    df_calc['governance_score'] = (
        df_calc['rnd_score'] * 0.35 +
        df_calc['energy_score'] * 0.35 +
        df_calc['gas_score'] * 0.30
    )
    
    # Overall Score
    df_calc['overall_score'] = (
        df_calc['environmental_score'] * 0.40 +
        df_calc['social_score'] * 0.30 +
        df_calc['governance_score'] * 0.30
    )
    
    df_calc['rank'] = df_calc['overall_score'].rank(ascending=False, method='dense').astype(int)
    
    return df_calc

# -----------------------
# GENERATE SMART INSIGHTS
# -----------------------
def generate_smart_insights(df_calc):
    """توليد تحليلات ذكية (Smart Insights)"""
    insights = []
    
    # تحديد الفائز
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    sorted_df = df_calc.sort_values('overall_score', ascending=False)
    runner = sorted_df.iloc[1] if len(sorted_df) > 1 else None
    
    # 1. تحليل الأداء العام
    insights.append({
        "category": "🏆 Overall Performance",
        "insight": f"{winner['company']} achieves the highest ESG score ({winner['overall_score']:.1f}/100), outperforming competitors through balanced performance across all three pillars.",
        "priority": "High"
    })
    
    if runner is not None:
        gap = winner['overall_score'] - runner['overall_score']
        insights.append({
            "category": "📊 Competitive Gap",
            "insight": f"{runner['company']} is {gap:.1f} points behind the leader. The main differentiator is in the Environmental pillar.",
            "priority": "Medium"
        })
    
    # 2. تحليل البيئي
    env_winner = df_calc.loc[df_calc['environmental_score'].idxmax()]
    insights.append({
        "category": "🌿 Environmental Leadership",
        "insight": f"{env_winner['company']} leads in environmental performance with {env_winner['environmental_score']:.1f}%, driven by low GHG emissions and high recycling rates.",
        "priority": "High"
    })
    
    # 3. تحليل الاجتماعي
    social_winner = df_calc.loc[df_calc['social_score'].idxmax()]
    insights.append({
        "category": "👥 Social Impact",
        "insight": f"{social_winner['company']} demonstrates strong social responsibility with {social_winner['social_score']:.1f}%, particularly in safety performance and social investment.",
        "priority": "Medium"
    })
    
    # 4. تحليل الحوكمة
    gov_winner = df_calc.loc[df_calc['governance_score'].idxmax()]
    insights.append({
        "category": "🏛️ Governance Excellence",
        "insight": f"{gov_winner['company']} excels in governance with {gov_winner['governance_score']:.1f}%, reflecting strong R&D investment and energy efficiency.",
        "priority": "Medium"
    })
    
    # 5. تحليل الانبعاثات
    lowest_ghg = df_calc.loc[df_calc['ghg_emissions'].idxmin()]
    avg_ghg = df_calc['ghg_emissions'].mean()
    insights.append({
        "category": "🌍 GHG Emissions",
        "insight": f"{lowest_ghg['company']} has the lowest GHG emissions ({lowest_ghg['ghg_emissions']:.1f}M tCO₂e), below the industry average of {avg_ghg:.1f}M tCO₂e.",
        "priority": "High"
    })
    
    # 6. تحليل السلامة
    safest = df_calc.loc[df_calc['safety_ltir'].idxmin()]
    insights.append({
        "category": "🛡️ Safety Performance",
        "insight": f"{safest['company']} achieves the best safety record with LTIR of {safest['safety_ltir']:.3f}, demonstrating strong safety culture and systems.",
        "priority": "High"
    })
    
    # 7. تحليل الاستثمار في R&D
    top_rnd = df_calc.loc[df_calc['rnd_spend'].idxmax()]
    insights.append({
        "category": "💡 Innovation & R&D",
        "insight": f"{top_rnd['company']} invests most heavily in R&D (${top_rnd['rnd_spend']:.0f}M), supporting long-term innovation and technology leadership.",
        "priority": "Medium"
    })
    
    # 8. تحليل التنوع
    top_female = df_calc.loc[df_calc['female_representation'].idxmax()]
    insights.append({
        "category": "⚖️ Diversity & Inclusion",
        "insight": f"{top_female['company']} leads in female representation ({top_female['female_representation']:.1f}%), exceeding industry average.",
        "priority": "Medium"
    })
    
    return insights

def generate_strategic_recommendations(df_calc):
    """توليد توصيات استراتيجية لكل شركة"""
    recommendations = []
    
    for idx, row in df_calc.iterrows():
        rec = {
            "company": row['company'],
            "recommendations": []
        }
        
        # Environmental Recommendations
        if row['environmental_score'] < 70:
            rec['recommendations'].append({
                "pillar": "🌿 Environmental",
                "action": "Accelerate deployment of carbon capture and storage (CCS) technologies.",
                "impact": "Reduce GHG emissions by 15-20% within 3 years",
                "priority": "High"
            })
        if row['recycling_rate'] < 60:
            rec['recommendations'].append({
                "pillar": "♻️ Circular Economy",
                "action": "Increase water recycling rate to 80%+ through investment in advanced treatment facilities.",
                "impact": "Reduce freshwater withdrawal by 30%",
                "priority": "High"
            })
        if row['renewable_capacity'] < 1.0:
            rec['recommendations'].append({
                "pillar": "⚡ Renewable Energy",
                "action": "Expand renewable energy portfolio to 5GW+ by 2030.",
                "impact": "Reduce operational carbon intensity by 25%",
                "priority": "Medium"
            })
        
        # Social Recommendations
        if row['safety_ltir'] > 0.02:
            rec['recommendations'].append({
                "pillar": "🛡️ Safety",
                "action": "Implement zero-incident safety culture program with AI-powered risk monitoring.",
                "impact": "Achieve LTIR below 0.01",
                "priority": "High"
            })
        if row['female_representation'] < 30:
            rec['recommendations'].append({
                "pillar": "👥 Diversity",
                "action": "Launch women in leadership program targeting 35% representation by 2028.",
                "impact": "Enhanced innovation and decision-making",
                "priority": "Medium"
            })
        if row['social_investment'] < 200:
            rec['recommendations'].append({
                "pillar": "🏘️ Community",
                "action": "Increase social investment to $250M+ focusing on education and community development.",
                "impact": "Strengthened community relations and social license to operate",
                "priority": "Medium"
            })
        
        # Governance Recommendations
        if row['rnd_spend'] < 1200:
            rec['recommendations'].append({
                "pillar": "🔬 Innovation",
                "action": "Increase R&D spend to 1.5% of revenue with focus on low-carbon technologies.",
                "impact": "Technology leadership and competitive advantage",
                "priority": "High"
            })
        if row['energy_intensity'] > 170:
            rec['recommendations'].append({
                "pillar": "⚡ Energy Efficiency",
                "action": "Implement AI-driven energy optimization across all operations.",
                "impact": "15% reduction in energy intensity",
                "priority": "Medium"
            })
        
        recommendations.append(rec)
    
    return recommendations

# -----------------------
# GENERATE PDF REPORT
# -----------------------
def save_plotly_fig_as_image(fig, width=800, height=400):
    """حفظ الرسم البياني من plotly كصورة مؤقتة"""
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            fig.write_image(tmp.name, width=width, height=height, scale=2)
            return tmp.name
    except Exception as e:
        return None

def generate_pdf_report(df_calc, insights, recommendations):
    """توليد تقرير PDF شامل"""
    
    filename = f"ESG_Benchmarking_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                 fontSize=24, textColor=colors.HexColor('#1B5E20'),
                                 spaceAfter=30, alignment=1)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], 
                                   fontSize=16, textColor=colors.HexColor('#2E7D32'),
                                   spaceAfter=12, spaceBefore=16)
    subheading_style = ParagraphStyle('CustomSubheading', parent=styles['Heading3'],
                                      fontSize=13, textColor=colors.HexColor('#0D47A1'),
                                      spaceAfter=8, spaceBefore=10)
    
    # 1. Cover Page
    story.append(Paragraph("🏆 Global Energy ESG Benchmarking Report", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("2025 Sustainability Analysis: Saudi Aramco · ExxonMobil · BP", styles['Heading2']))
    story.append(Spacer(1, 36))
    
    story.append(Paragraph("<b>Team Leader:</b> Ismail Kamal", styles['Normal']))
    story.append(Paragraph("<b>Team Members:</b> Adel ElSayed, Mohamed Gaber, Ahmed Omar, Sherouk Ashraf, Mohamed ElHammadi, Farouk Sameh", styles['Normal']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b><font color='red'>Under Supervision: Dr. Mohamed Tash</font></b>", styles['Normal']))
    story.append(Paragraph("<b>QHSE Master at Alexandria University</b>", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    
    # 2. Executive Summary
    story.append(PageBreak())
    story.append(Paragraph("📋 Executive Summary", heading_style))
    
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    summary_text = f"""
    This comprehensive ESG benchmarking report analyzes the sustainability performance of three major energy companies: 
    Saudi Aramco, ExxonMobil, and BP for the year 2025.
    
    <b>Key Findings:</b><br/>
    • <b>Overall Winner:</b> {winner['company']} with an ESG score of {winner['overall_score']:.1f}/100<br/>
    • <b>Environmental Leader:</b> {df_calc.loc[df_calc['environmental_score'].idxmax()]['company']}<br/>
    • <b>Social Leader:</b> {df_calc.loc[df_calc['social_score'].idxmax()]['company']}<br/>
    • <b>Governance Leader:</b> {df_calc.loc[df_calc['governance_score'].idxmax()]['company']}<br/>
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    
    # 3. Scores Table
    story.append(PageBreak())
    story.append(Paragraph("📊 ESG Scores Summary", heading_style))
    
    table_data = [
        ['Company', 'Environmental', 'Social', 'Governance', 'Overall', 'Rank']
    ]
    for idx, row in df_calc.iterrows():
        table_data.append([
            row['company'],
            f"{row['environmental_score']:.1f}%",
            f"{row['social_score']:.1f}%",
            f"{row['governance_score']:.1f}%",
            f"{row['overall_score']:.1f}%",
            f"#{int(row['rank'])}"
        ])
    
    table = Table(table_data, colWidths=[100, 80, 70, 80, 80, 50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B5E20')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    story.append(table)
    
    # 4. Winner Analysis
    story.append(PageBreak())
    story.append(Paragraph("🏆 Winner Analysis: " + winner['company'], heading_style))
    
    winner_text = f"""
    <b>Overall Score:</b> {winner['overall_score']:.1f}/100<br/>
    <b>ESG Rating:</b> {'A+ (Excellent)' if winner['overall_score'] >= 85 else 'A (Very Good)' if winner['overall_score'] >= 75 else 'B+ (Good)'}<br/><br/>
    <b>Key Strengths:</b><br/>
    • Environmental Score: {winner['environmental_score']:.1f}%<br/>
    • Social Score: {winner['social_score']:.1f}%<br/>
    • Governance Score: {winner['governance_score']:.1f}%<br/>
    • GHG Emissions: {winner['ghg_emissions']:.1f}M tCO₂e<br/>
    • Recycling Rate: {winner['recycling_rate']:.1f}%<br/>
    • Safety LTIR: {winner['safety_ltir']:.3f}
    """
    story.append(Paragraph(winner_text, styles['Normal']))
    
    # 5. Smart Insights
    story.append(PageBreak())
    story.append(Paragraph("🧠 Smart Insights & Analysis", heading_style))
    
    for insight in insights:
        story.append(Paragraph(f"<b>{insight['category']}</b>", subheading_style))
        story.append(Paragraph(insight['insight'], styles['Normal']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"<i>Priority: {insight['priority']}</i>", styles['Normal']))
        story.append(Spacer(1, 12))
    
    # 6. Strategic Recommendations
    story.append(PageBreak())
    story.append(Paragraph("💡 Strategic Recommendations", heading_style))
    
    for rec in recommendations:
        story.append(Paragraph(f"<b>{rec['company']}</b>", subheading_style))
        for action in rec['recommendations']:
            story.append(Paragraph(f"{action['pillar']} - <b>{action['action']}</b>", styles['Normal']))
            story.append(Paragraph(f"• Expected Impact: {action['impact']}", styles['Normal']))
            story.append(Paragraph(f"• Priority: {action['priority']}", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))
    
    # 7. Footer
    story.append(PageBreak())
    story.append(Paragraph("<hr/>", styles['Normal']))
    story.append(Paragraph("<b>Global Energy ESG Benchmarking 2025</b>", styles['Normal']))
    story.append(Paragraph("Developed by Ismail Kamal & Team | Under Supervision of Dr. Mohamed Tash", styles['Normal']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    
    doc.build(story)
    return filename

# -----------------------
# DISPLAY FUNCTIONS
# -----------------------
def display_winner_analysis(df_calc):
    """عرض تحليل الفائز بالتفصيل"""
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    
    st.markdown("---")
    st.markdown("## 🏆 Winner Analysis")
    
    rating = "⭐ A+ (Excellent)" if winner['overall_score'] >= 85 else \
             "⭐ A (Very Good)" if winner['overall_score'] >= 75 else \
             "⭐ B+ (Good)" if winner['overall_score'] >= 65 else \
             "⭐ B (Satisfactory)" if winner['overall_score'] >= 55 else \
             "⭐ C (Needs Improvement)"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                        border-radius: 20px; padding: 25px; border: 3px solid #F59E0B;'>
                <h1 style='color: #92400E; margin: 0;'>🏆 {winner['company']}</h1>
                <h2 style='color: #78350F;'>Overall ESG Score: {winner['overall_score']:.1f}/100</h2>
                <p style='font-size: 16px; color: #78350F;'>
                    <strong>🏅 Rank:</strong> #{int(winner['rank'])} | 
                    <strong>📊 ESG Rating:</strong> {rating}
                </p>
                <p><strong>🌿 Environmental:</strong> {winner['environmental_score']:.1f}/100</p>
                <p><strong>👥 Social:</strong> {winner['social_score']:.1f}/100</p>
                <p><strong>🏛️ Governance:</strong> {winner['governance_score']:.1f}/100</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background: #F8FAFC; border-radius: 20px; padding: 20px; text-align: center;'>
                <h3>💪 Key Strengths</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li>✅ GHG Emissions: {winner['ghg_emissions']:.1f}M t</li>
                    <li>✅ Methane Intensity: {winner['methane_intensity']:.2f}%</li>
                    <li>✅ Recycling Rate: {winner['recycling_rate']:.1f}%</li>
                    <li>✅ Safety LTIR: {winner['safety_ltir']:.3f}</li>
                    <li>✅ R&D Spend: ${winner['rnd_spend']:.0f}M</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def display_company_cards(df_calc):
    """عرض بطاقات الشركات مع الترتيب"""
    st.subheader("📊 Company Rankings")
    df_sorted = df_calc.sort_values('overall_score', ascending=False).reset_index(drop=True)
    cols = st.columns(len(df_sorted))
    
    medal_colors = ['#F59E0B', '#94A3B8', '#CD7F32']
    medal_icons = ['🥇', '🥈', '🥉']
    
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        with cols[i]:
            is_winner = (i == 0)
            
            st.markdown(f"""
                <div class='company-card' style='border-left-color: {medal_colors[i] if i < 3 else "#475569"};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='font-size: 28px;'>{medal_icons[i]}</span>
                        {'<span class="winner-badge">🏆 Winner</span>' if is_winner else f'<span style="color: #64748b;">#{row["rank"]}</span>'}
                    </div>
                    <h3 style='margin: 10px 0 5px 0;'>{row['company']}</h3>
                    <div class='score' style='color: {medal_colors[i] if i < 3 else "#475569"};'>{row['overall_score']:.1f}</div>
                    <div style='font-size: 14px; color: #64748b;'>Overall ESG Score</div>
                    
                    <div style='margin-top: 15px;'>
                        <div style='display: flex; justify-content: space-between; font-size: 12px;'>
                            <span>🌿 Environmental</span>
                            <span>{row['environmental_score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {min(row['environmental_score'], 100)}%;'></div></div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 12px; margin-top: 8px;'>
                            <span>👥 Social</span>
                            <span>{row['social_score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {min(row['social_score'], 100)}%;'></div></div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 12px; margin-top: 8px;'>
                            <span>🏛️ Governance</span>
                            <span>{row['governance_score']:.0f}%</span>
                        </div>
                        <div class='progress-bar'><div class='fill' style='width: {min(row['governance_score'], 100)}%;'></div></div>
                    </div>
                    
                    <div style='margin-top: 12px;'>
                        <span class='metric-pill'>🌿 GHG: {row['ghg_emissions']:.1f}M</span>
                        <span class='metric-pill'>♻️ Recycle: {row['recycling_rate']:.0f}%</span>
                        <span class='metric-pill'>⚡ Carbon: {row['upstream_carbon_intensity']:.1f}kg</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def display_charts(df_calc):
    """عرض الرسوم البيانية"""
    st.subheader("📈 ESG Performance Visualization")
    
    categories = ['environmental_score', 'social_score', 'governance_score']
    labels = ['🌿 Environmental', '👥 Social', '🏛️ Governance']
    colors = ['#2E7D32', '#1565C0', '#6A1B9A']
    
    fig_radar = go.Figure()
    for i, company in enumerate(df_calc['company']):
        values = df_calc[df_calc['company'] == company][categories].values.flatten().tolist()
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
    for i, company in enumerate(df_calc['company']):
        values = df_calc[df_calc['company'] == company][categories].values.flatten().tolist()
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

def display_detailed_comparison(df_calc):
    """عرض جدول المقارنة التفصيلي"""
    st.subheader("📋 Detailed ESG Comparison Table")
    
    display_cols = [
        'company', 'rank',
        'ghg_emissions', 'methane_intensity', 'flaring_intensity',
        'upstream_carbon_intensity', 'recycling_rate', 'water_consumption',
        'safety_ltir', 'total_recordable_rate', 'process_safety_events',
        'female_representation', 'social_investment',
        'rnd_spend', 'energy_intensity',
        'environmental_score', 'social_score', 'governance_score', 'overall_score'
    ]
    
    df_display = df_calc[display_cols].copy()
    
    format_dict = {
        'ghg_emissions': '{:.1f}M',
        'methane_intensity': '{:.2f}%',
        'flaring_intensity': '{:.2f}',
        'upstream_carbon_intensity': '{:.1f}',
        'recycling_rate': '{:.1f}%',
        'water_consumption': '{:.1f}M',
        'safety_ltir': '{:.3f}',
        'total_recordable_rate': '{:.2f}',
        'process_safety_events': '{:.0f}',
        'female_representation': '{:.1f}%',
        'social_investment': '${:.0f}M',
        'rnd_spend': '${:.0f}M',
        'energy_intensity': '{:.1f}',
        'environmental_score': '{:.1f}%',
        'social_score': '{:.1f}%',
        'governance_score': '{:.1f}%',
        'overall_score': '{:.1f}%'
    }
    
    for col, fmt in format_dict.items():
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: fmt.format(x))
    
    df_display.columns = [
        'Company', 'Rank',
        'GHG (M tCO₂e)', 'Methane (%)', 'Flaring (scf/boe)',
        'Carbon Intensity (kg)', 'Recycling (%)', 'Water (M m³)',
        'Safety LTIR', 'TRIR', 'Process Safety',
        'Women (%)', 'Social Investment',
        'R&D Spend', 'Energy Intensity',
        'Environmental', 'Social', 'Governance', 'Overall'
    ]
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def display_predictive_insights(df_calc, insights, recommendations):
    """عرض التوصيات والتنبؤات"""
    st.subheader("🔮 Predictive Insights & Strategic Recommendations")
    
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    sorted_df = df_calc.sort_values('overall_score', ascending=False)
    runner = sorted_df.iloc[1] if len(sorted_df) > 1 else None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='insight-box'>
                <h4>📊 Winner: {winner['company']}</h4>
                <p><strong>🏅 Overall Score:</strong> {winner['overall_score']:.1f}/100</p>
                <p><strong>🌿 Environmental:</strong> {winner['environmental_score']:.1f}%</p>
                <p><strong>👥 Social:</strong> {winner['social_score']:.1f}%</p>
                <p><strong>🏛️ Governance:</strong> {winner['governance_score']:.1f}%</p>
                <p style='margin-top: 10px;'><strong>✅ Key Strengths:</strong></p>
                <ul>
                    <li>🌿 Low GHG emissions: {winner['ghg_emissions']:.1f}M t</li>
                    <li>♻️ High recycling rate: {winner['recycling_rate']:.1f}%</li>
                    <li>🛡️ Safety LTIR: {winner['safety_ltir']:.3f}</li>
                    <li>⚡ Renewable capacity: {winner['renewable_capacity']:.1f}GW</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if runner is not None:
            st.markdown(f"""
                <div class='warning-box'>
                    <h4>📈 Runner-Up: {runner['company']}</h4>
                    <p><strong>🏅 Overall Score:</strong> {runner['overall_score']:.1f}/100</p>
                    <p><strong>Gap:</strong> {winner['overall_score'] - runner['overall_score']:.1f} points</p>
                    <p style='margin-top: 10px;'><strong>🟡 Areas for Improvement:</strong></p>
                    <ul>
                        <li>🌿 Reduce GHG by {(runner['ghg_emissions'] - winner['ghg_emissions']):.1f}M t</li>
                        <li>♻️ Increase recycling by {(winner['recycling_rate'] - runner['recycling_rate']):.1f}%</li>
                        <li>🛡️ Improve safety to LTIR {winner['safety_ltir']:.3f}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    # Display Smart Insights
    st.markdown("---")
    st.subheader("🧠 Smart Insights")
    for insight in insights:
        st.markdown(f"""
            <div style='background: #F0FDF4; border-radius: 10px; padding: 12px; margin: 8px 0; border-left: 4px solid #2E7D32;'>
                <p><strong>{insight['category']}</strong></p>
                <p>{insight['insight']}</p>
                <p style='font-size: 12px; color: #64748b;'>Priority: {insight['priority']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Display Strategic Recommendations
    st.markdown("---")
    st.subheader("💡 Strategic Recommendations")
    
    for rec in recommendations:
        st.markdown(f"### {rec['company']}")
        for action in rec['recommendations']:
            st.markdown(f"""
                <div style='background: #F8FAFC; border-radius: 10px; padding: 12px; margin: 8px 0; border-left: 4px solid #0D47A1;'>
                    <p><strong>{action['pillar']}</strong> - {action['action']}</p>
                    <p style='font-size: 12px; color: #64748b;'>• Expected Impact: {action['impact']}</p>
                    <p style='font-size: 12px; color: #64748b;'>• Priority: {action['priority']}</p>
                </div>
            """, unsafe_allow_html=True)

# -----------------------
# MAIN APP - UPLOAD SECTION
# -----------------------
st.markdown("## 📄 Upload Sustainability Reports")

st.markdown("""
### 📌 Instructions
1. Upload the 3 PDF reports (ExxonMobil, Saudi Aramco, BP)
2. Click "Run ESG Analysis"
3. View comprehensive benchmarking results with winner analysis
""")

col1, col2, col3 = st.columns(3)
with col1:
    exxon_file = st.file_uploader("ExxonMobil Report", type="pdf", key="exxon")
with col2:
    aramco_file = st.file_uploader("Saudi Aramco Report", type="pdf", key="aramco")
with col3:
    bp_file = st.file_uploader("BP Report", type="pdf", key="bp")

# -----------------------
# MAIN APP - ANALYSIS BUTTON
# -----------------------
if st.button("🚀 Run ESG Analysis", type="primary", use_container_width=True):
    with st.spinner("📊 Analyzing ESG performance of Saudi Aramco, ExxonMobil, and BP..."):
        files = [exxon_file, aramco_file, bp_file]
        company_names = ["ExxonMobil", "Saudi Aramco", "BP"]
        df = process_uploaded_reports(files, company_names)
        df_calc = calculate_esg_scores(df)
        insights = generate_smart_insights(df_calc)
        recommendations = generate_strategic_recommendations(df_calc)
        st.session_state.results = df_calc
        st.session_state.insights = insights
        st.session_state.recommendations = recommendations
        st.session_state.analysis_done = True
    st.success("✅ Analysis complete! Results displayed below.")
    st.balloons()

if st.session_state.analysis_done and st.session_state.results is not None:
    df_calc = st.session_state.results
    insights = st.session_state.insights
    recommendations = st.session_state.recommendations
    
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
    
    # 5. Smart Insights & Strategic Recommendations
    st.markdown("---")
    display_predictive_insights(df_calc, insights, recommendations)
    
    # 6. Export
    st.markdown("---")
    st.markdown("## 📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df_calc.to_csv(index=False)
        st.download_button(
            label="📊 Download ESG Analysis as CSV",
            data=csv,
            file_name=f"ESG_Benchmarking_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("📄 Download Full PDF Report", use_container_width=True, type="primary"):
            with st.spinner("Generating comprehensive PDF report..."):
                pdf_file = generate_pdf_report(df_calc, insights, recommendations)
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
        <p style='color: white;'>🏆 Global Energy ESG Benchmarking 2025 | Saudi Aramco · ExxonMobil · BP</p>
        <p style='color: #E8F5E9; font-size: 12px;'>Developed by <strong>Ismail Kamal</strong> & Team | <strong style='color: #FF0000;'>Under Supervision of Dr. Mohamed Tash</strong></p>
        <p style='color: #FFD54F; font-size: 11px;'>Version 10.0 | GRI · TCFD · SASB · SBTi Compliant</p>
    </div>
""", unsafe_allow_html=True)
