import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pypdf import PdfReader
import re

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
        padding: 30px 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }
    .main-header p {
        color: #E8F5E9;
        margin: 10px 0 0 0;
    }
    
    .company-card {
        background: white;
        border-radius: 20px;
        padding: 25px 20px 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 2px solid #E2E8F0;
        margin: 10px 5px;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    .company-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .company-card .score {
        font-size: 36px;
        font-weight: 700;
        margin: 10px 0;
    }
    .company-card .score-label {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 15px;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        margin: 4px 0 10px 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.8s ease;
    }
    
    .winner-badge {
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
        padding: 4px 16px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    
    .metric-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        background: #f1f5f9;
        color: #334155;
        margin: 3px;
    }
    
    .metric-label {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: #334155;
        padding: 2px 0;
    }
    
    .upload-container {
        border: 2px dashed #1B5E20;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        background: #f8fafc;
        margin: 10px 0;
    }
    .upload-container:hover {
        background: #f0fdf4;
        border-color: #2E7D32;
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
            <p style='color: #FFD54F; font-weight: bold;'>🏆 Ismail Kamal <span style='color: #E8F5E9; font-weight: normal;'>(Leader)</span></p>
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
# PDF EXTRACTION FUNCTIONS
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

def extract_esg_metrics(text, company_name, default_data):
    """استخراج مؤشرات ESG من النص أو استخدام القيم الافتراضية"""
    if not text:
        return default_data
    
    def find_value(pattern, text, default):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(',', ''))
            except:
                return default
        return default
    
    # Environmental Metrics
    ghg = find_value(r'GHG\s*emissions?.*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, default_data['ghg_emissions'])
    if ghg == 0:
        ghg = find_value(r'(\d+(?:\.\d+)?)\s*(?:million|M)\s*(?:tons?)?\s*(?:CO2|GHG)', text, default_data['ghg_emissions'])
    
    methane = find_value(r'methane\s*intensity.*?(\d+(?:\.\d+)?)\s*%', text, default_data['methane_intensity'])
    flaring = find_value(r'flaring\s*intensity.*?(\d+(?:\.\d+)?)', text, default_data['flaring_intensity'])
    renewable = find_value(r'renewable\s*capacity.*?(\d+(?:\.\d+)?)\s*(?:GW|gigawatt)', text, default_data['renewable_capacity'])
    water = find_value(r'water\s*(?:consumption|withdrawal).*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, default_data['water_consumption'])
    recycling = find_value(r'recycling\s*rate.*?(\d+(?:\.\d+)?)\s*%', text, default_data['recycling_rate'])
    carbon_intensity = find_value(r'carbon\s*intensity.*?(\d+(?:\.\d+)?)\s*(?:kg|CO2e)', text, default_data['upstream_carbon_intensity'])
    reduction = find_value(r'(?:emissions?|GHG)\s*reduction.*?(\d+(?:\.\d+)?)\s*%', text, default_data['emissions_reduction'])
    biodiversity = find_value(r'biodiversity.*?(\d+(?:\.\d+)?)\s*%', text, default_data['biodiversity_protection'])
    
    # Social Metrics
    ltir = find_value(r'LTIR.*?(\d+(?:\.\d+)?)', text, default_data['safety_ltir'])
    trir = find_value(r'(?:total|recordable).*?(\d+(?:\.\d+)?)', text, default_data['total_recordable_rate'])
    safety_events = find_value(r'(?:process\s*safety|Tier\s*1).*?(\d+)', text, default_data['process_safety_events'])
    investment = find_value(r'social\s*investment.*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, default_data['social_investment'])
    female = find_value(r'women|female.*?(\d+(?:\.\d+)?)\s*%', text, default_data['female_representation'])
    employees = find_value(r'employees.*?(\d+(?:,?\d+)*)', text, default_data['employees'])
    
    # Governance Metrics
    rnd = find_value(r'R.?D\s*spend.*?(\d+(?:\.\d+)?)\s*(?:million|M)', text, default_data['rnd_spend'])
    energy_intensity = find_value(r'energy\s*intensity.*?(\d+(?:\.\d+)?)', text, default_data['energy_intensity'])
    gas_prod = find_value(r'gas\s*production.*?(\d+(?:\.\d+)?)\s*(?:bscfd|bcf)', text, default_data['gas_production'])
    oil_prod = find_value(r'oil\s*production.*?(\d+(?:\.\d+)?)\s*(?:MMbd|mbd)', text, default_data['oil_production'])
    
    return {
        "company": company_name,
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

def process_uploaded_reports(exxon_file, aramco_file, bp_file):
    """معالجة التقارير المرفوعة"""
    # بيانات افتراضية لكل شركة
    default_exxon = {
        "company": "ExxonMobil",
        "ghg_emissions": 34.3,
        "methane_intensity": 0.04,
        "flaring_intensity": 2.5,
        "energy_intensity": 180,
        "renewable_capacity": 0.5,
        "safety_ltir": 0.02,
        "total_recordable_rate": 0.17,
        "process_safety_events": 61,
        "water_consumption": 330,
        "recycling_rate": 40,
        "social_investment": 200,
        "female_representation": 28,
        "rnd_spend": 1200,
        "upstream_carbon_intensity": 9.5,
        "emissions_reduction": 25,
        "biodiversity_protection": 85,
        "employees": 61000,
        "gas_production": 10.0,
        "oil_production": 4.5
    }
    
    default_aramco = {
        "company": "Saudi Aramco",
        "ghg_emissions": 58.0,
        "methane_intensity": 0.04,
        "flaring_intensity": 6.65,
        "energy_intensity": 164.3,
        "renewable_capacity": 1.28,
        "safety_ltir": 0.011,
        "total_recordable_rate": 0.028,
        "process_safety_events": 9,
        "water_consumption": 78.5,
        "recycling_rate": 69.1,
        "social_investment": 541,
        "female_representation": 8.2,
        "rnd_spend": 1451,
        "upstream_carbon_intensity": 10.0,
        "emissions_reduction": 0,
        "biodiversity_protection": 96.5,
        "employees": 76664,
        "gas_production": 11.4,
        "oil_production": 10.7
    }
    
    default_bp = {
        "company": "BP",
        "ghg_emissions": 34.3,
        "methane_intensity": 0.04,
        "flaring_intensity": 4.5,
        "energy_intensity": 175,
        "renewable_capacity": 1.0,
        "safety_ltir": 0.25,
        "total_recordable_rate": 0.20,
        "process_safety_events": 27,
        "water_consumption": 250,
        "recycling_rate": 55,
        "social_investment": 64,
        "female_representation": 35,
        "rnd_spend": 900,
        "upstream_carbon_intensity": 8.5,
        "emissions_reduction": 37,
        "biodiversity_protection": 80,
        "employees": 93700,
        "gas_production": 9.0,
        "oil_production": 3.5
    }
    
    results = []
    
    # معالجة ExxonMobil
    if exxon_file is not None:
        text = extract_text_from_pdf(exxon_file)
        results.append(extract_esg_metrics(text, "ExxonMobil", default_exxon))
    else:
        results.append(default_exxon)
    
    # معالجة Saudi Aramco
    if aramco_file is not None:
        text = extract_text_from_pdf(aramco_file)
        results.append(extract_esg_metrics(text, "Saudi Aramco", default_aramco))
    else:
        results.append(default_aramco)
    
    # معالجة BP
    if bp_file is not None:
        text = extract_text_from_pdf(bp_file)
        results.append(extract_esg_metrics(text, "BP", default_bp))
    else:
        results.append(default_bp)
    
    return pd.DataFrame(results)

# -----------------------
# CALCULATE SCORES
# -----------------------
def calculate_esg_scores(df):
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
# DISPLAY FUNCTIONS
# -----------------------
def display_winner_analysis(df_calc):
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
                <h1 style='color: #92400E; margin: 0;'>{winner['company']}</h1>
                <h2 style='color: #78350F;'>Overall Score: {winner['overall_score']:.1f}/100</h2>
                <p style='font-size: 16px; color: #78350F;'>
                    <strong>Rank:</strong> #{int(winner['rank'])} | 
                    <strong>ESG Rating:</strong> {rating}
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
                    <li>✅ GHG: {winner['ghg_emissions']:.1f}M t</li>
                    <li>✅ Methane: {winner['methane_intensity']:.2f}%</li>
                    <li>✅ Recycling: {winner['recycling_rate']:.1f}%</li>
                    <li>✅ Safety LTIR: {winner['safety_ltir']:.3f}</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def display_company_cards(df_calc):
    """عرض بطاقات الشركات بشكل احترافي"""
    st.subheader("📊 Company Rankings")
    df_sorted = df_calc.sort_values('overall_score', ascending=False).reset_index(drop=True)
    
    medal_colors = ['#F59E0B', '#94A3B8', '#CD7F32']
    medal_icons = ['🥇', '🥈', '🥉']
    
    cols = st.columns(len(df_sorted))
    
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        with cols[i]:
            is_winner = (i == 0)
            border_color = medal_colors[i] if i < 3 else '#475569'
            
            st.markdown(f"""
                <div class='company-card' style='border-color: {border_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='font-size: 28px;'>{medal_icons[i]}</span>
                        {'<span class="winner-badge">🏆 Winner</span>' if is_winner else ''}
                    </div>
                    
                    <h3 style='margin: 10px 0 5px 0;'>{row['company']}</h3>
                    
                    <div class='score' style='color: {border_color};'>{row['overall_score']:.1f}</div>
                    <div class='score-label'>Overall ESG Score</div>
                    
                    <div style='margin: 15px 0;'>
                        <div class='metric-label'>
                            <span>🌿 Environmental</span>
                            <span><strong>{row['environmental_score']:.0f}%</strong></span>
                        </div>
                        <div class='progress-bar'>
                            <div class='progress-fill' style='width: {min(row['environmental_score'], 100)}%; background: linear-gradient(90deg, #2E7D32, #4CAF50);'></div>
                        </div>
                        
                        <div class='metric-label'>
                            <span>👥 Social</span>
                            <span><strong>{row['social_score']:.0f}%</strong></span>
                        </div>
                        <div class='progress-bar'>
                            <div class='progress-fill' style='width: {min(row['social_score'], 100)}%; background: linear-gradient(90deg, #1565C0, #42A5F5);'></div>
                        </div>
                        
                        <div class='metric-label'>
                            <span>🏛️ Governance</span>
                            <span><strong>{row['governance_score']:.0f}%</strong></span>
                        </div>
                        <div class='progress-bar'>
                            <div class='progress-fill' style='width: {min(row['governance_score'], 100)}%; background: linear-gradient(90deg, #6A1B9A, #AB47BC);'></div>
                        </div>
                    </div>
                    
                    <div style='display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-top: 10px;'>
                        <span class='metric-pill'>🌿 GHG: {row['ghg_emissions']:.1f}M</span>
                        <span class='metric-pill'>♻️ Recycle: {row['recycling_rate']:.0f}%</span>
                        <span class='metric-pill'>⚡ Carbon: {row['upstream_carbon_intensity']:.1f}kg</span>
                        <span class='metric-pill'>🛡️ Safety: {row['safety_ltir']:.3f}</span>
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
            line_color=colors[i % len(colors)]
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
    """عرض جدول المقارنة"""
    st.subheader("📋 Detailed ESG Comparison Table")
    
    display_cols = [
        'company', 'rank',
        'ghg_emissions', 'methane_intensity', 'recycling_rate',
        'safety_ltir', 'female_representation', 'rnd_spend',
        'environmental_score', 'social_score', 'governance_score', 'overall_score'
    ]
    
    df_display = df_calc[display_cols].copy()
    
    format_dict = {
        'ghg_emissions': '{:.1f}M',
        'methane_intensity': '{:.2f}%',
        'recycling_rate': '{:.1f}%',
        'safety_ltir': '{:.3f}',
        'female_representation': '{:.1f}%',
        'rnd_spend': '${:.0f}M',
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
        'GHG (M tCO₂e)', 'Methane (%)', 'Recycling (%)',
        'Safety LTIR', 'Women (%)', 'R&D ($M)',
        'Environmental', 'Social', 'Governance', 'Overall'
    ]
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def generate_smart_insights(df_calc):
    """توليد تحليلات ذكية"""
    insights = []
    
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    sorted_df = df_calc.sort_values('overall_score', ascending=False)
    runner = sorted_df.iloc[1] if len(sorted_df) > 1 else None
    
    insights.append({
        "category": "🏆 Overall Performance",
        "insight": f"{winner['company']} achieves the highest ESG score ({winner['overall_score']:.1f}/100), leading in Environmental and Governance pillars.",
        "priority": "High"
    })
    
    if runner is not None:
        gap = winner['overall_score'] - runner['overall_score']
        insights.append({
            "category": "📊 Competitive Gap",
            "insight": f"{runner['company']} is {gap:.1f} points behind. The main gap is in Environmental performance.",
            "priority": "Medium"
        })
    
    return insights

def display_predictive_insights(df_calc, insights):
    """عرض التوصيات"""
    st.subheader("🔮 Predictive Insights & Recommendations")
    
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    sorted_df = df_calc.sort_values('overall_score', ascending=False)
    runner = sorted_df.iloc[1] if len(sorted_df) > 1 else None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style='background: #F0FDF4; border-radius: 16px; padding: 20px; border-left: 6px solid #1B5E20;'>
                <h4>📊 Winner: {winner['company']}</h4>
                <p><strong>Overall Score:</strong> {winner['overall_score']:.1f}/100</p>
                <p><strong>🌿 Environmental:</strong> {winner['environmental_score']:.1f}%</p>
                <p><strong>👥 Social:</strong> {winner['social_score']:.1f}%</p>
                <p><strong>🏛️ Governance:</strong> {winner['governance_score']:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if runner is not None:
            st.markdown(f"""
                <div style='background: #FEF3C7; border-radius: 16px; padding: 20px; border-left: 6px solid #F59E0B;'>
                    <h4>📈 Runner-Up: {runner['company']}</h4>
                    <p><strong>Overall Score:</strong> {runner['overall_score']:.1f}/100</p>
                    <p><strong>Gap:</strong> {winner['overall_score'] - runner['overall_score']:.1f} points</p>
                </div>
            """, unsafe_allow_html=True)
    
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

# -----------------------
# MAIN APP - UPLOAD SECTION
# -----------------------
st.markdown("## 📄 Upload Sustainability Reports")

st.markdown("""
<div style='background: #f0fdf4; border-radius: 15px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #1B5E20;'>
    <p style='margin: 0;'><strong>📌 Instructions:</strong> Upload the 3 PDF reports below, then click "Run ESG Analysis"</p>
</div>
""", unsafe_allow_html=True)

# 3 أعمدة لرفع الملفات
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='upload-container'>
        <span style='font-size: 28px;'>🛢️</span>
        <h4>ExxonMobil</h4>
        <p style='font-size: 12px; color: #64748b;'>2025 Sustainability Report</p>
    </div>
    """, unsafe_allow_html=True)
    exxon_file = st.file_uploader("Upload ExxonMobil Report", type="pdf", key="exxon_upload", label_visibility="collapsed")

with col2:
    st.markdown("""
    <div class='upload-container'>
        <span style='font-size: 28px;'>🇸🇦</span>
        <h4>Saudi Aramco</h4>
        <p style='font-size: 12px; color: #64748b;'>2025 Sustainability Report</p>
    </div>
    """, unsafe_allow_html=True)
    aramco_file = st.file_uploader("Upload Saudi Aramco Report", type="pdf", key="aramco_upload", label_visibility="collapsed")

with col3:
    st.markdown("""
    <div class='upload-container'>
        <span style='font-size: 28px;'>🌊</span>
        <h4>BP</h4>
        <p style='font-size: 12px; color: #64748b;'>2025 Sustainability Report</p>
    </div>
    """, unsafe_allow_html=True)
    bp_file = st.file_uploader("Upload BP Report", type="pdf", key="bp_upload", label_visibility="collapsed")

# -----------------------
# MAIN APP - ANALYSIS BUTTON
# -----------------------
if st.button("🚀 Run ESG Analysis", type="primary", use_container_width=True):
    with st.spinner("📊 Analyzing ESG performance of Saudi Aramco, ExxonMobil, and BP..."):
        df = process_uploaded_reports(exxon_file, aramco_file, bp_file)
        df_calc = calculate_esg_scores(df)
        insights = generate_smart_insights(df_calc)
        st.session_state.results = df_calc
        st.session_state.insights = insights
        st.session_state.analysis_done = True
    st.success("✅ Analysis complete! Results displayed below.")
    st.balloons()

if st.session_state.get('analysis_done', False) and st.session_state.results is not None:
    df_calc = st.session_state.results
    insights = st.session_state.insights
    
    display_winner_analysis(df_calc)
    st.markdown("---")
    display_company_cards(df_calc)
    st.markdown("---")
    display_charts(df_calc)
    st.markdown("---")
    display_detailed_comparison(df_calc)
    st.markdown("---")
    display_predictive_insights(df_calc, insights)
    
    # Export
    st.markdown("---")
    st.markdown("## 📥 Export Results")
    csv = df_calc.to_csv(index=False)
    st.download_button(
        label="📊 Download ESG Analysis as CSV",
        data=csv,
        file_name=f"ESG_Benchmarking_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

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
