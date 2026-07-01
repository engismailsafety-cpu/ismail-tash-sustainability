# -*- coding: utf-8 -*-
"""
app.py
======
Professional ESG Benchmarking Platform v11.0
SOHE Master's Program — Alexandria University

تحسينات هذه النسخة عن النسخة السابقة (Deepseek v10):
  1. نظام استخراج هجين (Hybrid Extraction): محاولة Regex من PDF المرفوع،
     مع رجوع تلقائي (fallback) لقاعدة بيانات موثّقة يدويًا بدلًا من
     قيم افتراضية وهمية.
  2. تتبّع مصدر كل رقم (Source Traceability): كل قيمة في التقرير النهائي
     مرفقة بحالتها (مُستخرج آليًا / من قاعدة البيانات الموثقة / غير متاح)
     ورقم الصفحة عند توفره.
  3. تطبيع صريح وموثّق (Documented Normalization) قبل أي مقارنة كمية بين
     شركات تستخدم تعريفات قياس مختلفة جوهريًا (LTIR مقابل TRCR مقابل RIF).
  4. عرض "تنبيهات عدم تجانس القياس" (Non-Comparability Warnings) تلقائيًا.
  5. رسوم بيانية احترافية متعددة (Radar, Grouped Bar, Heatmap مطبّع).
  6. تقرير PDF كامل جاهز للطباعة، يتضمن الرسوم البيانية + جدول المصادر.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
import io
import os
import tempfile
from datetime import datetime

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, KeepTogether
)
from reportlab.lib.units import cm

from verified_data import VERIFIED_ESG_DATABASE, NORMALIZED_COMPARISON

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="Professional ESG Benchmarking Platform v11",
    page_icon="🏆",
    layout="wide",
)

PRIMARY_GRAD = "linear-gradient(135deg, #0D47A1 0%, #1B5E20 100%)"

st.markdown(f"""
    <style>
    .main-header {{
        background: {PRIMARY_GRAD};
        padding: 32px 24px; border-radius: 18px; margin-bottom: 26px;
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    .main-header h1 {{ color: white; margin: 0; font-size: 32px; font-weight: 700; }}
    .main-header p {{ color: #E8F5E9; margin: 10px 0 0 0; }}

    .source-badge {{
        display:inline-block; padding:2px 10px; border-radius:14px;
        font-size:11px; font-weight:600; margin-left:6px;
    }}
    .badge-verified {{ background:#DCFCE7; color:#166534; }}
    .badge-extracted {{ background:#DBEAFE; color:#1E40AF; }}
    .badge-missing {{ background:#FEE2E2; color:#991B1B; }}

    .warn-box {{
        background:#FFFBEB; border-left:5px solid #F59E0B;
        padding:14px 18px; border-radius:10px; margin:10px 0; font-size:14px;
    }}
    .company-card {{
        background:white; border-radius:18px; padding:20px;
        box-shadow:0 4px 18px rgba(0,0,0,0.08); border-left:6px solid #1B5E20;
        margin:8px 0;
    }}
    .metric-pill {{
        display:inline-block; padding:4px 12px; border-radius:18px;
        font-size:12px; background:#F1F5F9; margin:3px;
    }}
    </style>
""", unsafe_allow_html=True)

COMPANY_LIST = ["ExxonMobil", "Saudi Aramco", "BP"]

# =====================================================================
# SESSION STATE
# =====================================================================
for key, default in [
    ("analysis_done", False),
    ("results", None),
    ("source_log", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# =====================================================================
# CORE: PDF TEXT EXTRACTION
# =====================================================================
def extract_text_from_pdf(file) -> str:
    """يحاول استخراج النص الكامل من ملف PDF مرفوع. يرجع نص فارغ عند الفشل."""
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
    except Exception:
        return ""


def safe_extract_number(pattern, text, flags=re.IGNORECASE | re.DOTALL):
    """استخراج رقم بصيغة آمنة. يرجع None (وليس صفرًا وهميًا) عند الفشل."""
    try:
        match = re.search(pattern, text, flags)
        if match:
            for group in match.groups():
                if group is not None:
                    clean = re.sub(r"[^\d.]", "", str(group))
                    if clean and clean != ".":
                        return float(clean)
        return None
    except Exception:
        return None


# نمط Regex لكل مؤشر — تُستخدم كمحاولة أولى قبل الرجوع لقاعدة البيانات الموثقة
REGEX_PATTERNS = {
    "Safety_LTIR_or_TRCR": r"(?:LTIR|lost.time\s*incident\s*rate|total\s*recordable\s*case\s*rate)\D{0,40}(\d+\.\d+)",
    "Methane_Intensity_Pct": r"methane\s*intensity\D{0,30}(\d+\.\d+)\s*%",
    "Diversity_Women_Pct": r"(?:female|women)\D{0,30}representation\D{0,20}(\d+(?:\.\d+)?)\s*%",
    "Social_Investment_M": r"social\s*investment\D{0,30}\$?\s*(\d+(?:\.\d+)?)\s*(?:million|M\b)",
    "Recycling_Pct": r"recycl(?:ing|ed)\D{0,30}(\d+(?:\.\d+)?)\s*%",
    "Upstream_Carbon_Intensity": r"upstream\s*carbon\s*intensity\D{0,30}(\d+\.\d+)\s*kg",
}


def attempt_regex_extraction(text: str) -> dict:
    """محاولة استخراج آلي أولي. يرجع قاموسًا بالقيم التي تم العثور عليها فعليًا فقط."""
    found = {}
    for key, pattern in REGEX_PATTERNS.items():
        val = safe_extract_number(pattern, text)
        if val is not None:
            found[key] = val
    return found


# =====================================================================
# CORE: HYBRID DATA RESOLUTION (Regex → Verified DB → Missing)
# =====================================================================
def resolve_company_data(company_name: str, uploaded_text: str):
    """
    يبني سجل بيانات الشركة بمنهجية هجينة:
      1) يحاول الاستخراج الآلي من النص المرفوع.
      2) عند الفشل، يرجع لقاعدة البيانات الموثقة يدويًا (مع ذكر المصدر والصفحة).
      3) عند غياب الاثنين، يُسجَّل المؤشر كـ "غير متاح" صراحة (لا قيم وهمية).
    يُرجع: (record, source_log)
    """
    verified = VERIFIED_ESG_DATABASE.get(company_name, {})
    verified_metrics = verified.get("metrics", {})
    extracted = attempt_regex_extraction(uploaded_text) if uploaded_text else {}

    record = {"Company": company_name}
    source_log = {}

    mapping = [
        ("Scope1_Emissions", "Scope1_Emissions_MMtCO2e", "Scope1_Emissions_MtCO2e"),
        ("Methane_Intensity_Pct", "Upstream_Methane_Intensity_Pct", "Methane_Intensity_Pct"),
        ("Safety_Rate", "Safety_TRCR", "Safety_RIF"),
        ("Safety_Rate_Alt", "Safety_LTI_Rate", None),
        ("Diversity_Women_Pct", "Diversity_Women_Workforce_Pct", "Diversity_Women_Workforce_Pct"),
        ("Social_Investment_M", "Social_Investment_USD_Million", "Social_Investment_USD_Million"),
        ("Recycling_Pct", "Industrial_Waste_Recycled_Pct", "Waste_Recycled_Recovered_Pct"),
        ("Upstream_Carbon_Intensity", "Upstream_Carbon_Intensity", None),
        ("Fatalities", "Fatalities_Total", "Fatalities_Total"),
        ("Process_Safety_Events", "Tier1_Process_Safety_Events", "Tier1_2_Process_Safety_Events"),
    ]

    exxon_alias = {
        "Scope1_Emissions": None,
        "Methane_Intensity_Pct": None,
        "Safety_Rate": "Safety_LTIR",
        "Safety_Rate_Alt": None,
        "Diversity_Women_Pct": "Diversity_Women_Workforce_Pct",
        "Social_Investment_M": "Social_Investment_USD_Million",
        "Recycling_Pct": "Recycling_Rate_Lubricants",
        "Upstream_Carbon_Intensity": None,
        "Fatalities": "Fatalities_Total",
        "Process_Safety_Events": "Process_Safety_Events_HighConsequence",
    }

    regex_key_map = {
        "Safety_Rate": "Safety_LTIR_or_TRCR",
        "Methane_Intensity_Pct": "Methane_Intensity_Pct",
        "Diversity_Women_Pct": "Diversity_Women_Pct",
        "Social_Investment_M": "Social_Investment_M",
        "Recycling_Pct": "Recycling_Pct",
        "Upstream_Carbon_Intensity": "Upstream_Carbon_Intensity",
    }

    for display_key, key_for_others, key_for_bp in mapping:
        regex_key = regex_key_map.get(display_key)

        value = None
        status = "missing"
        page_ref = None
        note = ""

        # 1) محاولة الاستخراج الآلي أولًا (فقط لو فيه نص مرفوع فعلي)
        if regex_key and regex_key in extracted:
            value = extracted[regex_key]
            status = "extracted"

        # 2) الرجوع لقاعدة البيانات الموثقة
        if value is None:
            if company_name == "ExxonMobil":
                lookup_key = exxon_alias.get(display_key)
            elif company_name == "BP":
                lookup_key = key_for_bp
            else:  # Saudi Aramco
                lookup_key = key_for_others

            if lookup_key and lookup_key in verified_metrics:
                meta = verified_metrics[lookup_key]
                if meta.get("value") is not None:
                    value = meta["value"]
                    status = "verified_db"
                    page_ref = meta.get("page")
                    note = meta.get("note", "")

        record[display_key] = value
        source_log[display_key] = {
            "status": status, "page": page_ref, "note": note,
            "report": verified.get("report_title", ""),
        }

    return record, source_log


# =====================================================================
# CORE: SCORING (with explicit normalization documentation)
# =====================================================================
def calculate_professional_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    يحسب درجات ESG مركّبة بعد تطبيع صريح للمؤشرات (Min-Max 0-100).
    القيم المفقودة لا تُستبدل بقيم افتراضية وهمية؛ بدلًا من ذلك تُستبعد
    من حساب متوسط ذلك البُعد (mean of available, skipna=True).
    """
    d = df.copy()

    def normalize_lower_is_better(series):
        s = pd.to_numeric(series, errors="coerce")
        valid = s.dropna()
        if valid.empty or valid.max() == valid.min():
            return pd.Series([np.nan] * len(s), index=s.index)
        return (1 - (s - valid.min()) / (valid.max() - valid.min())) * 100

    def normalize_higher_is_better(series):
        s = pd.to_numeric(series, errors="coerce")
        valid = s.dropna()
        if valid.empty or valid.max() == valid.min():
            return pd.Series([np.nan] * len(s), index=s.index)
        return ((s - valid.min()) / (valid.max() - valid.min())) * 100

    d["Score_Safety"] = normalize_lower_is_better(d["Safety_Rate"])
    d["Score_Methane"] = normalize_lower_is_better(d["Methane_Intensity_Pct"])
    d["Score_Recycling"] = normalize_higher_is_better(d["Recycling_Pct"])
    d["Score_CarbonIntensity"] = normalize_lower_is_better(d["Upstream_Carbon_Intensity"])

    d["Score_Diversity"] = normalize_higher_is_better(d["Diversity_Women_Pct"])
    d["Score_SocialInvestment"] = normalize_higher_is_better(d["Social_Investment_M"])
    d["Score_FatalitiesInv"] = normalize_lower_is_better(d["Fatalities"])

    d["Score_ProcessSafety"] = normalize_lower_is_better(d["Process_Safety_Events"])

    env_cols = ["Score_Methane", "Score_Recycling", "Score_CarbonIntensity"]
    soc_cols = ["Score_Diversity", "Score_SocialInvestment", "Score_FatalitiesInv"]
    gov_cols = ["Score_Safety", "Score_ProcessSafety"]

    d["Environmental_Score"] = d[env_cols].mean(axis=1, skipna=True)
    d["Social_Score"] = d[soc_cols].mean(axis=1, skipna=True)
    d["Governance_Score"] = d[gov_cols].mean(axis=1, skipna=True)

    d["Overall_Score"] = d[["Environmental_Score", "Social_Score", "Governance_Score"]].mean(
        axis=1, skipna=True
    )
    d["Rank"] = d["Overall_Score"].rank(ascending=False, method="dense").astype(int)
    return d


NORMALIZATION_METHOD_DOC = """
**منهجية التطبيع المُستخدمة (Normalization Methodology):**

نظرًا لاختلاف تعريفات القياس الأصلية جذريًا بين الشركات الثلاث
(مثال: السلامة تُقاس عند ExxonMobil بـ LTIR، وعند Aramco بـ TRCR/LTI rate،
وعند BP بـ RIF غير مُفصح رقميًا في النص المتاح)، يطبّق هذا التطبيق
خطوة **Min-Max Normalization** صريحة لكل عمود على حدة (0-100) بدلاً من
مقارنة الأرقام الخام مباشرة. القيم المفقودة لا تُستبدل بقيم افتراضية؛
بل تُستبعد من حساب متوسط ذلك البُعد لتلك الشركة، ويُذكر ذلك صراحة في
تقرير المصادر (Source Log) المرفق.

⚠️ هذا التطبيع **لا يلغي** الفروق الجوهرية في طريقة قياس كل شركة لمؤشراتها؛
هو فقط يجعل المقارنة الكمية ممكنة إحصائيًا، مع الإبقاء على الأرقام
الأصلية ظاهرة دائمًا للمراجع الأكاديمي.
"""
