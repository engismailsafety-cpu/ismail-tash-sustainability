import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

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
# DATA EXTRACTION FROM REPORTS
# -----------------------
@st.cache_data
def get_company_data():
    """بيانات مستخرجة من تقارير 2025 للشركات الثلاث"""
    
    # أرامكو (Saudi Aramco)
    aramco = {
        "company": "Saudi Aramco",
        "industry": "Oil & Gas",
        "ghg_emissions": 58.0,  # مليون طن CO2e
        "methane_intensity": 0.04,  # %
        "flaring_intensity": 6.65,  # scf/boe
        "energy_intensity": 164.3,  # kBtu/boe
        "renewable_capacity": 1.28,  # GW
        "safety_ltir": 0.011,  # Lost Time Injury Rate
        "total_recordable_rate": 0.028,  # TRIR
        "process_safety_events": 9,  # Tier 1
        "water_consumption": 78.5,  # مليون m3
        "recycling_rate": 69.1,  # %
        "social_investment": 541,  # مليون دولار
        "female_representation": 8.2,  # %
        "rnd_spend": 1451,  # مليون دولار
        "upstream_carbon_intensity": 10.0,  # kg CO2e/boe
        "emissions_reduction": 0.0,  # نسبة التخفيض (خط الأساس)
        "biodiversity_protection": 96.5,  # %
        "employees": 76664,
        "gas_production": 11.4,  # bscfd
        "oil_production": 10.7,  # MMbd
    }
    
    # إكسون موبيل (ExxonMobil)
    exxon = {
        "company": "ExxonMobil",
        "industry": "Oil & Gas",
        "ghg_emissions": 34.3,  # مليون طن CO2e (2024)
        "methane_intensity": 0.04,  # % (تقديري)
        "flaring_intensity": 2.5,  # scf/boe (تقديري)
        "energy_intensity": 180.0,  # kBtu/boe (تقديري)
        "renewable_capacity": 0.5,  # GW
        "safety_ltir": 0.02,  # Lost Time Injury Rate
        "total_recordable_rate": 0.17,  # TRIR
        "process_safety_events": 61,  # Tier 1
        "water_consumption": 330,  # مليون m3 (تقديري)
        "recycling_rate": 40,  # % (تقديري)
        "social_investment": 200,  # مليون دولار
        "female_representation": 28,  # %
        "rnd_spend": 1200,  # مليون دولار
        "upstream_carbon_intensity": 9.5,  # kg CO2e/boe (تقديري)
        "emissions_reduction": 25,  # % تخفيض من 2016
        "biodiversity_protection": 85,  # %
        "employees": 61000,
        "gas_production": 10.0,  # bscfd (تقديري)
        "oil_production": 4.5,  # MMbd (تقديري)
    }
    
    # بي بي (BP)
    bp = {
        "company": "BP",
        "industry": "Oil & Gas",
        "ghg_emissions": 34.3,  # مليون طن CO2e (2025)
        "methane_intensity": 0.04,  # %
        "flaring_intensity": 4.5,  # scf/boe (تقديري)
        "energy_intensity": 175.0,  # kBtu/boe (تقديري)
        "renewable_capacity": 1.0,  # GW
        "safety_ltir": 0.25,  # Lost Time Injury Rate
        "total_recordable_rate": 0.20,  # TRIR
        "process_safety_events": 27,  # Tier 1+2
        "water_consumption": 250,  # مليون m3 (تقديري)
        "recycling_rate": 55,  # %
        "social_investment": 64,  # مليون دولار
        "female_representation": 35,  # %
        "rnd_spend": 900,  # مليون دولار
        "upstream_carbon_intensity": 8.5,  # kg CO2e/boe (تقديري)
        "emissions_reduction": 37,  # % تخفيض من 2019
        "biodiversity_protection": 80,  # %
        "employees": 93700,
        "gas_production": 9.0,  # bscfd (تقديري)
        "oil_production": 3.5,  # MMbd (تقديري)
    }
    
    return pd.DataFrame([aramco, exxon, bp])

def calculate_esg_scores(df):
    """حساب درجات ESG مع أوزان مخصصة"""
    df_calc = df.copy()
    
    # ========== Environmental Score (40%) ==========
    # 1. GHG Emissions (معكوس - الأقل أفضل)
    max_ghg = max(df_calc['ghg_emissions'].max(), 1)
    df_calc['ghg_score'] = (1 - (df_calc['ghg_emissions'] / max_ghg)) * 100
    
    # 2. Methane Intensity (معكوس)
    max_methane = max(df_calc['methane_intensity'].max(), 0.01)
    df_calc['methane_score'] = (1 - (df_calc['methane_intensity'] / max_methane)) * 100
    
    # 3. Flaring Intensity (معكوس)
    max_flaring = max(df_calc['flaring_intensity'].max(), 1)
    df_calc['flaring_score'] = (1 - (df_calc['flaring_intensity'] / max_flaring)) * 100
    
    # 4. Renewable Capacity (مباشر)
    max_renewable = max(df_calc['renewable_capacity'].max(), 1)
    df_calc['renewable_score'] = (df_calc['renewable_capacity'] / max_renewable) * 100
    
    # 5. Water Consumption (معكوس)
    max_water = max(df_calc['water_consumption'].max(), 1)
    df_calc['water_score'] = (1 - (df_calc['water_consumption'] / max_water)) * 100
    
    # 6. Recycling Rate (مباشر)
    max_recycling = max(df_calc['recycling_rate'].max(), 1)
    df_calc['recycling_score'] = (df_calc['recycling_rate'] / max_recycling) * 100
    
    # 7. Upstream Carbon Intensity (معكوس)
    max_carbon = max(df_calc['upstream_carbon_intensity'].max(), 1)
    df_calc['carbon_intensity_score'] = (1 - (df_calc['upstream_carbon_intensity'] / max_carbon)) * 100
    
    # 8. Emissions Reduction (مباشر)
    max_reduction = max(df_calc['emissions_reduction'].max(), 1)
    df_calc['reduction_score'] = (df_calc['emissions_reduction'] / max_reduction) * 100
    
    # 9. Biodiversity Protection (مباشر)
    max_biodiversity = max(df_calc['biodiversity_protection'].max(), 1)
    df_calc['biodiversity_score'] = (df_calc['biodiversity_protection'] / max_biodiversity) * 100
    
    # Environmental Score
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
    
    # ========== Social Score (30%) ==========
    # Safety LTIR (معكوس)
    max_ltir = max(df_calc['safety_ltir'].max(), 0.01)
    df_calc['safety_score'] = (1 - (df_calc['safety_ltir'] / max_ltir)) * 100
    
    # Total Recordable Rate (معكوس)
    max_trir = max(df_calc['total_recordable_rate'].max(), 0.01)
    df_calc['trir_score'] = (1 - (df_calc['total_recordable_rate'] / max_trir)) * 100
    
    # Process Safety Events (معكوس)
    max_events = max(df_calc['process_safety_events'].max(), 1)
    df_calc['safety_events_score'] = (1 - (df_calc['process_safety_events'] / max_events)) * 100
    
    # Social Investment (مباشر)
    max_investment = max(df_calc['social_investment'].max(), 1)
    df_calc['investment_score'] = (df_calc['social_investment'] / max_investment) * 100
    
    # Female Representation (مباشر)
    max_female = max(df_calc['female_representation'].max(), 1)
    df_calc['female_score'] = (df_calc['female_representation'] / max_female) * 100
    
    # Employees (مباشر - حجم القوى العاملة)
    max_employees = max(df_calc['employees'].max(), 1)
    df_calc['employees_score'] = (df_calc['employees'] / max_employees) * 100
    
    # Social Score
    df_calc['social_score'] = (
        df_calc['safety_score'] * 0.25 +
        df_calc['trir_score'] * 0.15 +
        df_calc['safety_events_score'] * 0.15 +
        df_calc['investment_score'] * 0.20 +
        df_calc['female_score'] * 0.15 +
        df_calc['employees_score'] * 0.10
    )
    
    # ========== Governance Score (30%) ==========
    # R&D Spend (مباشر)
    max_rnd = max(df_calc['rnd_spend'].max(), 1)
    df_calc['rnd_score'] = (df_calc['rnd_spend'] / max_rnd) * 100
    
    # Energy Intensity (معكوس - الكفاءة)
    max_energy = max(df_calc['energy_intensity'].max(), 1)
    df_calc['energy_score'] = (1 - (df_calc['energy_intensity'] / max_energy)) * 100
    
    # Gas Production (مباشر - مؤشر على التحول للغاز)
    max_gas = max(df_calc['gas_production'].max(), 1)
    df_calc['gas_score'] = (df_calc['gas_production'] / max_gas) * 100
    
    # Governance Score
    df_calc['governance_score'] = (
        df_calc['rnd_score'] * 0.35 +
        df_calc['energy_score'] * 0.35 +
        df_calc['gas_score'] * 0.30
    )
    
    # ========== Overall Score ==========
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
    
    # Radar Chart
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
    
    # Bar Chart
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

def display_predictive_insights(df_calc):
    """عرض التوصيات والتنبؤات"""
    st.subheader("🔮 Predictive Insights & Strategic Recommendations")
    
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    runner = df_calc.loc[df_calc['overall_score'].idxmax() - 1] if len(df_calc) > 1 else None
    
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
    
    # Recommendations
    st.markdown("""
        <div style='background: #F8FAFC; border-radius: 16px; padding: 20px; margin-top: 15px; border: 1px solid #E2E8F0;'>
            <h4>💡 Strategic Recommendations</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;'>
                <div>
                    <strong>🌿 Environmental</strong>
                    <ul>
                        <li>Accelerate CCS deployment</li>
                        <li>Increase renewable share</li>
                        <li>Enhance water recycling</li>
                    </ul>
                </div>
                <div>
                    <strong>👥 Social</strong>
                    <ul>
                        <li>Improve diversity to 35%+</li>
                        <li>Increase social investment</li>
                        <li>Enhance safety culture</li>
                    </ul>
                </div>
                <div>
                    <strong>🏛️ Governance</strong>
                    <ul>
                        <li>Increase R&D investment</li>
                        <li>Improve energy efficiency</li>
                        <li>Expand gas portfolio</li>
                    </ul>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------
# MAIN APP
# -----------------------
st.markdown("## 📊 ESG Benchmarking Analysis")

if st.button("🚀 Run ESG Analysis", type="primary", use_container_width=True):
    with st.spinner("📊 Analyzing ESG performance of Saudi Aramco, ExxonMobil, and BP..."):
        df = get_company_data()
        df_calc = calculate_esg_scores(df)
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
