import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #1C1F26;
}

/* HEADINGS */
h1, h2, h3 {
    color: white;
    font-weight: bold;
}

/* METRIC CARDS */
[data-testid="metric-container"] {
    background-color: #1C1F26;
    border: 1px solid #31333F;
    padding: 15px;
    border-radius: 12px;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #31333F;
    border-radius: 10px;
}

/* BUTTONS */
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}

/* DOWNLOAD BUTTON */
.stDownloadButton>button {
    background-color: #00C853;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}

/* SELECT BOX */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1C1F26;
}

/* SLIDERS */
.stSlider {
    color: #FF4B4B;
}

.feature-card{
    transition: all 0.3s ease;
}

.feature-card:hover{
    transform: translateY(-12px) scale(1.02);
    border: 1px solid #3B82F6;
    box-shadow: 0 0 30px rgba(59,130,246,0.6);
}

div.stButton > button:first-child {
    background: linear-gradient(90deg,#7C3AED,#EC4899);
    color: white;
    border: none;
    border-radius: 12px;
    height: 55px;
    font-size: 18px;
    font-weight: 600;
    transition: all 0.3s ease;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0px 0px 20px rgba(236,72,153,0.5);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Mutual Fund Screener",
    layout="wide"
)

st.markdown("""
<div style='text-align:center;'>

<h1 style='
color:white;
font-size:55px;
margin-bottom:5px;
'>
📈 Mutual Fund Intelligence Platform
</h1>

<p style='
font-size:22px;
color:#A0AEC0;
'>
Screen • Compare • Analyze • Recommend
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background: linear-gradient(90deg,#1E3A8A,#2563EB);
padding:20px;
border-radius:15px;
margin-bottom:25px;
text-align:center;
">
<h3 style="color:white;">
🚀 Discover High Quality Mutual Funds Using Data-Driven Screening
</h3>
<p style="color:white;">
Compare funds, evaluate risk, analyze portfolio allocation and shortlist the best investment opportunities.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:#1C1F26;
padding:20px;
border-radius:15px;
border:1px solid #31333F;
margin-top:20px;
margin-bottom:20px;
text-align:center;
">
<h2>🧠 Investor Risk Profiler</h2>
<p>Answer a few questions to determine your investment risk appetite.</p>
</div>
""", unsafe_allow_html=True)

if st.button(
    "🧠 Start Risk Assessment",
    use_container_width=True
):
    st.session_state["show_risk"] = True

if st.session_state.get("show_risk", False):

    total_score = 0

    st.subheader("Investor Details")

    client_name = st.text_input("Investor Name")

    st.markdown("---")

    st.subheader("Question 1")

    q1_options = [
        "Stable returns with minimal fluctuations",
        "Moderate returns with limited fluctuations",
        "Balanced growth over long term",
        "Higher long-term growth despite market volatility"
    ]

    q1 = st.radio(
        "What kind of investment experience are you looking for?",
        q1_options
    )

    score_q1 = {
        "Stable returns with minimal fluctuations": 1,
        "Moderate returns with limited fluctuations": 2,
        "Balanced growth over long term": 3,
        "Higher long-term growth despite market volatility": 4
    }[q1]

    total_score += score_q1

    st.subheader("Question 2")

    q2 = st.radio(
        "What is your ideal investment horizon?",
        [
            "Less than 1 year",
            "1 - 3 years",
            "3 - 5 years",
            "More than 5 years"
        ]
    )

    score_q2 = {
        "Less than 1 year": 1,
        "1 - 3 years": 2,
        "3 - 5 years": 3,
        "More than 5 years": 4
    }[q2]

    total_score += score_q2

    st.subheader("Question 3")

    q3 = st.radio(
        "How comfortable are you with short-term fluctuations?",
        [
            "Not comfortable",
            "Comfortable with small fluctuations",
            "Comfortable with moderate fluctuations",
            "Comfortable with high fluctuations for long-term growth"
        ]
    )

    score_q3 = {
        "Not comfortable": 1,
        "Comfortable with small fluctuations": 2,
        "Comfortable with moderate fluctuations": 3,
        "Comfortable with high fluctuations for long-term growth": 4
    }[q3]

    total_score += score_q3

    st.subheader("Question 4")

    q4 = st.radio(
        "If your investment value falls by 10-15%, what would you most likely do?",
        [
            "Redeem all investments",
            "Redeem a portion",
            "Stay invested",
            "Invest more during market correction"
        ]
    )

    score_q4 = {
        "Redeem all investments": 1,
        "Redeem a portion": 2,
        "Stay invested": 3,
        "Invest more during market correction": 4
    }[q4]

    total_score += score_q4

    st.subheader("Question 5")

    q5 = st.radio(
        "What percentage of your monthly income can you comfortably invest regularly?",
        [
            "Less than 5%",
            "5% - 10%",
            "10% - 20%",
            "More than 20%"
        ]
    )

    score_q5 = {
        "Less than 5%": 1,
        "5% - 10%": 2,
        "10% - 20%": 3,
        "More than 20%": 4
    }[q5]

    total_score += score_q5

    st.subheader("Question 6")

    q6 = st.radio(
        "How would you describe your attitude towards investment risk?",
        [
            "I prefer safety over returns",
            "I can take limited risk for slightly better returns",
            "I can tolerate moderate market fluctuations",
            "I am comfortable with high volatility for potentially higher returns"
        ]
    )

    score_q6 = {
        "I prefer safety over returns": 1,
        "I can take limited risk for slightly better returns": 2,
        "I can tolerate moderate market fluctuations": 3,
        "I am comfortable with high volatility for potentially higher returns": 4
    }[q6]

    total_score += score_q6

    if st.button("📊 Calculate Risk Score"):

        if total_score <= 9:
            risk = "Conservative"
            scheme = "Liquid Funds, Ultra Short Duration Funds, Debt Funds"
            color = "#00cc00"

        elif total_score <= 14:
            risk = "Moderately Conservative"
            scheme = "Large Cap Funds, Corporate Bond Funds, Conservative Hybrid Funds"
            color = "#A3E635"

        elif total_score <= 18:
            risk = "Moderate"
            scheme = "Balanced Advantage Funds, Aggressive Hybrid Funds, Multi Asset Funds"
            color = "#F59E0B"

        elif total_score <= 21:
            risk = "Moderately Aggressive"
            scheme = "Flexi Cap Funds, Large & Mid Cap Funds, Multi Cap Funds"
            color = "#F97316"

        else:
            risk = "Aggressive"
            scheme = "Mid Cap Funds, Small Cap Funds, Sectoral/Thematic Funds"
            color = "#EF4444"

        st.markdown(f"""
        <div style="
        background:{color};
        padding:20px;
        border-radius:15px;
        margin-top:20px;
        text-align:center;
        ">
        <h2>🛡 Risk Profile Result</h2>
        
        <div style="
        display:inline-block;
        background:white;
        color:black;
        padding:8px 20px;
        border-radius:30px;
        font-weight:bold;
        font-size:18px;
        margin-top:10px;
        margin-bottom:10px;
        ">
        {risk}
        </div>

        <p><b>Recommended Fund Categories:</b></p>
        <p>{scheme}</p>
        </div>
        """, unsafe_allow_html=True)

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(pdf_buffer)

        styles = getSampleStyleSheet()

        from reportlab.lib import colors

        styles['Heading1'].textColor = colors.darkblue
        styles['Heading2'].textColor = colors.darkblue
        styles['Heading3'].textColor = colors.black

        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER

        center_style = ParagraphStyle(
            'CenterStyle',
            parent=styles['Title'],
            alignment=TA_CENTER
        )

        if risk == "Conservative":
                summary = "Focuses on capital preservation and stability. Suitable for investors with low risk tolerance."

        elif risk == "Moderately Conservative":
            summary = "Prefers stable growth with limited market fluctuations."

        elif risk == "Moderate":
            summary = "Seeks a balance between capital appreciation and risk management."

        else:
            summary = "Comfortable with higher volatility in pursuit of long-term wealth creation."

        logo_path = os.path.join(
            os.path.dirname(__file__),
            "logo.png"
        )

        # st.write(logo_path)

        logo = Image(
            logo_path,
            width=120,
            height=120
        )

        content = [

            logo,

            Spacer(1,10),

            Paragraph(
                "<font size=24 color='darkblue'><b>RUSHHABH FINANCIAL SERVICES</b></font>",
                center_style
            ),

        Spacer(1,12),

            Paragraph(
                "<font size=18><b>Mutual Fund Risk Assessment Report</b></font>",
                center_style
            ),

            Paragraph("-" * 80, styles['BodyText']),
            Paragraph("INVESTOR DETAILS", styles['Heading2']),
            Paragraph("-" * 80, styles['BodyText']),
            Spacer(1,10),

            Paragraph(f"<b>Investor Name:</b> {client_name}", styles['BodyText']),
            Paragraph(f"<b>Assessment Date:</b> {datetime.now().strftime('%d-%m-%Y')}", styles['BodyText']),
            Paragraph(
                f"Report ID: RFS-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                styles['BodyText']
            ),
            Paragraph("<b>Advisor:</b> Rushhabh Financial Services", styles['BodyText']),

            Spacer(1,10),

            Paragraph("-" * 80, styles['BodyText']),
            Paragraph(
                "<font color='darkblue'><b>RISK PROFILE SUMMARY</b></font>",
                styles['Heading2']
            ),
            Paragraph("-" * 80, styles['BodyText']),
            Spacer(1,10),

            Paragraph(f"■ Risk Score: {total_score}/24", styles['BodyText']),

            Paragraph(
                f"<font size=20 color='darkblue'><b>Risk Category: {risk}</b></font>",
                center_style
            ),
            Paragraph(f"■ Recommended Categories: {scheme}", styles['BodyText']),
            Paragraph(" ", styles['BodyText']),
            Paragraph("<b>Risk Interpretation</b>", styles['Heading3']),
            Paragraph(summary, styles['BodyText']),

            Paragraph("Investment Suitability Conclusion", styles['Heading2']),

            Paragraph(
                f"Based on the responses provided, the investor falls under the "
                f"<b>{risk}</b> risk profile category. The suggested mutual fund "
                f"categories align with the investor's stated risk tolerance and "
                f"investment objectives.",
                styles['BodyText']
            ),

            Spacer(1,6),

            Paragraph("Risk Assessment Summary", styles['Heading2']),

            Paragraph("-" * 80, styles['BodyText']),
            Paragraph("INVESTOR RESPONSES", styles['Heading2']),
            Paragraph("-" * 80, styles['BodyText']),

            Paragraph("<b>Question 1</b>", styles['Heading3']),
            Paragraph("What kind of investment experience are you looking for?", styles['BodyText']),
            Paragraph(f"✓ <b>Selected Answer:</b> {q1}", styles['BodyText']),
            Spacer(1,12),

            Paragraph("<b>Question 2</b>", styles['Heading3']),
            Paragraph("What is your ideal investment horizon?", styles['BodyText']),
            Paragraph(f"✓ <b>Selected Answer:</b> {q2}", styles['BodyText']),
            Spacer(1,12),

            Paragraph("<b>Question 3</b>", styles['Heading3']),
            Paragraph("How comfortable are you with short-term fluctuations?", styles['BodyText']),
            Paragraph(f"✓ <b>Selected Answer:</b> {q3}", styles['BodyText']),
            Spacer(1,12),

            Paragraph("<b>Question 4</b>", styles['Heading3']),
            Paragraph("If your investment value falls by 10-15%, what would you most likely do?", styles['BodyText']),
            Paragraph(f"✓ <b>Selected Answer:</b> {q4}", styles['BodyText']),
            Spacer(1,12),

            Paragraph("<b>Question 5</b>", styles['Heading3']),
            Paragraph("What percentage of your monthly income can you comfortably invest regularly?", styles['BodyText']),
            Paragraph(f"✓ <b>Selected Answer:</b> {q5}", styles['BodyText']),
            Spacer(1,12),

            Paragraph("<b>Question 6</b>", styles['Heading3']),
            Paragraph("How would you describe your attitude towards investment risk?", styles['BodyText']),
            Paragraph(f"✓ <b>Selected Answer:</b> {q6}", styles['BodyText']),
            Spacer(1,12),

            Spacer(1,20),

            Paragraph("Disclaimer", styles['Heading2']),

            Paragraph(
                "This risk assessment is intended solely for investor profiling purposes. "
                "It should not be construed as investment advice or a recommendation to buy or sell any security. "
                "Mutual fund investments are subject to market risks. Please read all scheme-related documents carefully before investing.",
                styles['BodyText']
            ),


            Spacer(1,30),

            Paragraph("Investor Signature", styles['Heading3']),
            Paragraph("_________________________", styles['BodyText']),

            Spacer(1,20),

            Paragraph("Authorized Advisor", styles['Heading3']),
            Paragraph("Rushhabh Financial Services", styles['BodyText']),
            Paragraph("_________________________", styles['BodyText']),

            Spacer(1,30),

            Paragraph(
                "Generated by Rushhabh Financial Services",
                styles['Italic']
            ),

            Paragraph(
                "For educational and assessment purposes only.",
                styles['Italic']
            )            

        ]
            
        doc.build(content)

        pdf_buffer.seek(0)

        st.download_button(
            label="📥 Download Risk Assessment Report",
            data=pdf_buffer,
            file_name="Risk_Profile_Report.pdf",
            mime="application/pdf"
        )

        
        if total_score <= 9:
            risk = "Conservative"
            scheme = "Liquid Funds, Ultra Short Duration Funds, Debt Funds"
            color = "#2ECC71"

        elif total_score <= 14:
            risk = "Moderately Conservative"
            scheme = "Large Cap Funds, Corporate Bond Funds, Conservative Hybrid Funds"
            color = "#A3E635"

        elif total_score <= 18:
            risk = "Moderate"
            scheme = "Balanced Advantage Funds, Aggressive Hybrid Funds, Multi Asset Funds"
            color = "#F59E0B"

        elif total_score <= 21:
            risk = "Moderately Aggressive"
            scheme = "Flexi Cap Funds, Large & Mid Cap Funds, Multi Cap Funds"
            color = "#F97316"

        else:
            risk = "Aggressive"
            scheme = "Mid Cap Funds, Small Cap Funds, Sectoral/Thematic Funds"
            color = "#EF4444"

        if risk == "Conservative":
            summary = "The investor demonstrates a preference for capital preservation and lower volatility over aggressive growth."

        elif risk == "Moderately Conservative":
            summary = "The investor is willing to accept limited risk in pursuit of slightly higher returns."

        elif risk == "Moderate":
            summary = "The investor seeks a balance between growth and stability and can tolerate moderate market fluctuations."

        else:
            summary = "The investor is comfortable with significant market volatility in pursuit of long-term capital appreciation."
            
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card" style="
    background:#1C1F26;
    padding:25px;
    border-radius:15px;
    text-align:center;
    border:1px solid #31333F;
    ">
    <h2>📊</h2>
    <h4 style="color:white;">Fund Screening</h4>
    <p style="color:#A0AEC0;">
    Find the best mutual funds using CAGR, Sharpe Ratio and Beta filters.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" style="
    background:#1C1F26;
    padding:25px;
    border-radius:15px;
    text-align:center;
    border:1px solid #31333F;
    ">
    <h2>⚖️</h2>
    <h4 style="color:white;">Fund Comparison</h4>
    <p style="color:#A0AEC0;">
    Compare two funds side-by-side and identify the better performer.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card" style="
    background:#1C1F26;
    padding:25px;
    border-radius:15px;
    text-align:center;
    border:1px solid #31333F;
    ">
    <h2>🎯</h2>
    <h4 style="color:white;">Portfolio Analysis</h4>
    <p style="color:#A0AEC0;">
    Analyze Large Cap, Mid Cap, Small Cap and Cash allocation.
    </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FILE UPLOADER
# =====================================================

st.markdown("""
<div style="
background:#1C1F26;
padding:12px;
border-radius:20px;
border:1px solid #31333F;
text-align:center;
margin-top:20px;
margin-bottom:5px;
">

<h2 style="color:white;">
📂 Upload Mutual Fund Dataset
</h2>

<p style="color:#A0AEC0;font-size:18px;">
Upload your Excel file to start screening,
comparing and analyzing mutual funds.
</p>

<p style="color:#6B7280;">
Supported Format: XLSX
</p>

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose Excel File",
    type=["xlsx"],
    label_visibility="collapsed"
)

st.markdown("""
<div style="
display:flex;
justify-content:space-between;
gap:15px;
margin-top:20px;
margin-bottom:25px;
">

<div style="
flex:1;
background:#1C1F26;
padding:15px;
border-radius:12px;
text-align:center;
border:1px solid #31333F;
">
<h3>📊 500+</h3>
<p>Funds Analyzed</p>
</div>

<div style="
flex:1;
background:#1C1F26;
padding:15px;
border-radius:12px;
text-align:center;
border:1px solid #31333F;
">
<h3>📈 CAGR</h3>
<p>Based Screening</p>
</div>

<div style="
flex:1;
background:#1C1F26;
padding:15px;
border-radius:12px;
text-align:center;
border:1px solid #31333F;
">
<h3>⚠ Risk</h3>
<p>Analysis Engine</p>
</div>

<div style="
flex:1;
background:#1C1F26;
padding:15px;
border-radius:12px;
text-align:center;
border:1px solid #31333F;
">
<h3>⚖ Compare</h3>
<p>Funds Side-by-Side</p>
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# MAIN PROGRAM
# =====================================================

if uploaded_file:

    tab1, tab2 = st.tabs(
        ["Fund Screener", "Compare Funds"]
    )

    with tab1:

        # =================================================
        # LOAD EXCEL FILE
        # =================================================

            excel_file = pd.ExcelFile(uploaded_file)

            # REMOVE GRAPH / HOME SHEETS
            sheet_names = [
                sheet for sheet in excel_file.sheet_names
                if "graph" not in sheet.lower()
                and "home" not in sheet.lower()
            ]

        # =================================================
        # SELECT SHEET
        # =================================================

            selected_sheet = st.selectbox(
                "Select Sheet",
                sheet_names
            )

        # =================================================
        # READ EXCEL
        # =================================================

            raw_df = pd.read_excel(
                uploaded_file,
                sheet_name=selected_sheet,
                header=None
            )

        # REMOVE FULL EMPTY ROWS
            raw_df = raw_df.dropna(how="all")

        # =================================================
        # ACTUAL DATA STARTS FROM ROW 4
        # =================================================

            clean_df = raw_df.iloc[4:].reset_index(drop=True)

        # =================================================
        # KEEP FIRST 17 COLUMNS
        # =================================================

            clean_df = clean_df.iloc[:, :17]

        # =================================================
        # CORRECT COLUMN NAMES
        # =================================================

            clean_df.columns = [
                "Scheme Name",
                "NAV",
                "Inception Date",
                "Fund Size (Rs. Crs.)",
                "3 Years CAGR",
                "5 Years CAGR",
                "10 Years CAGR",
                "Since Inception",
                "Equity %",
                "Cash/Others %",
                "Std Dev",
                "Sharpe",
                "Beta",
                "Large Cap %",
                "Mid Cap %",
                "Small Cap %",
                "Fund Manager"
            ]

        # =================================================
        # KEEP IMPORTANT COLUMNS
        # =================================================

            clean_df = clean_df[
                [
                    "Scheme Name",
                    "NAV",
                    "Inception Date",
                    "Fund Size (Rs. Crs.)",
                    "3 Years CAGR",
                    "5 Years CAGR",
                    "10 Years CAGR",
                    "Since Inception",
                    "Equity %",
                    "Cash/Others %",
                    "Std Dev",
                    "Sharpe",
                    "Beta",
                    "Large Cap %",
                    "Mid Cap %",
                    "Small Cap %",
                    "Fund Manager"
                ]
            ]

        # =================================================
        # REMOVE EMPTY ROWS
        # =================================================

            clean_df = clean_df[
                clean_df["Scheme Name"].notna()
            ]

        # =================================================
        # REMOVE UNWANTED ROWS
        # =================================================

            remove_keywords = [
                "Regular Schemes",
                "Direct Schemes",
                "Peer Group Average",
                "Median",
                "Nifty",
                "BSE",
                "TRI",
                "Sensex"
            ]

            for keyword in remove_keywords:

                clean_df = clean_df[
                    ~clean_df["Scheme Name"].astype(str).str.contains(
                        keyword,
                        case=False,
                        na=False
                    )
                ]

        # =================================================
        # CONVERT NUMERIC COLUMNS
        # =================================================

            numeric_cols = [
                "NAV",
                "Fund Size (Rs. Crs.)",
                "3 Years CAGR",
                "5 Years CAGR",
                "10 Years CAGR",
                "Since Inception",
                "Equity %",
                "Cash/Others %",
                "Std Dev",
                "Sharpe",
                "Beta",
                "Large Cap %",
                "Mid Cap %",
                "Small Cap %"
            ]

            for col in numeric_cols:

                clean_df[col] = pd.to_numeric(
                    clean_df[col],
                    errors="coerce"
                )

        # =================================================
        # REMOVE ROWS WHERE CAGR IS EMPTY
        # =================================================

            clean_df = clean_df[
                clean_df["3 Years CAGR"].notna()
            ]

        # =================================================
        # PEER GROUP AVERAGES
        # =================================================

            avg_3y = clean_df["3 Years CAGR"].mean()
            avg_5y = clean_df["5 Years CAGR"].mean()
            avg_10y = clean_df["10 Years CAGR"].mean()

            st.subheader("Peer Group Averages")

            st.write(f"3 Years CAGR Average: {avg_3y:.2f}")
            st.write(f"5 Years CAGR Average: {avg_5y:.2f}")
            st.write(f"10 Years CAGR Average: {avg_10y:.2f}")

        # =================================================
        # DISPLAY CLEAN DATA
        # =================================================

            st.subheader(f"{selected_sheet} Clean Data")

            st.dataframe(
                clean_df,
                use_container_width=True,
                height=400
            )

        # =================================================
        # SIDEBAR FILTERS
        # =================================================

            st.sidebar.header("Screening Filters")

            # STEP 1 → FUND SIZE
            min_fund_size = st.sidebar.number_input(
                "Minimum Fund Size (Rs. Cr.)",
                min_value=0,
                value=1000
            )

            # STEP 2 → BETA
            max_beta = st.sidebar.slider(
                "Maximum Beta",
                min_value=0.0,
                max_value=3.0,
                value=1.0,
                step=0.1
            )

            # STEP 3 → SHARPE
            min_sharpe = st.sidebar.slider(
                "Minimum Sharpe Ratio",
                min_value=-5.0,
                max_value=5.0,
                value=0.0,
                step=0.1
            )

            # STEP 4 → 3 YEAR CAGR
            enable_3y = st.sidebar.checkbox(
                "Apply 3 Years CAGR Filter",
                value=True
            )

            # STEP 5 → 5 YEAR CAGR
            enable_5y = st.sidebar.checkbox(
                "Apply 5 Years CAGR Filter",
                value=True
            )

            # STEP 6 → 10 YEAR CAGR
            enable_10y = st.sidebar.checkbox(
                "Apply 10 Years CAGR Filter",
                value=True
            )

        # =================================================
        # SCREENING LOGIC
        # =================================================

            shortlisted_df = clean_df.copy()
            # =====================================================
            # SEARCH BOX
            # =====================================================

            search_term = st.text_input(
                "Search Fund Name"
            )

            if search_term:

                shortlisted_df = shortlisted_df[
                    shortlisted_df["Scheme Name"]
                    .str.contains(
                        search_term,
                        case=False,
                        na=False
                    )
                ]

            # STEP 1 → REMOVE FUNDS BELOW MINIMUM SIZE
            shortlisted_df = shortlisted_df[
                shortlisted_df["Fund Size (Rs. Crs.)"] >= min_fund_size
            ]

            # STEP 2 → REMOVE FUNDS WITH HIGH BETA
            shortlisted_df = shortlisted_df[
                shortlisted_df["Beta"] <= max_beta
            ]
        # =================================================
        # RISK CATEGORY
        # =================================================

            def risk_category(beta):

                if beta < 0.9:
                    return "Low Risk"

                elif beta <= 1.1:
                    return "Moderate Risk"

                else:
                    return "High Risk"

            shortlisted_df["Risk Level"] = shortlisted_df["Beta"].apply(
                risk_category
            )
            # STEP 3 → REMOVE NEGATIVE SHARPE
            shortlisted_df = shortlisted_df[
                shortlisted_df["Sharpe"] >= min_sharpe
            ]

            # STEP 4 → 3 YEAR CAGR FILTER
            if enable_3y:

                shortlisted_df = shortlisted_df[
                    shortlisted_df["3 Years CAGR"] >= avg_3y
                ]

            # STEP 5 → 5 YEAR CAGR FILTER
            if enable_5y:

                shortlisted_df = shortlisted_df[
                    shortlisted_df["5 Years CAGR"] >= avg_5y
                ]

            # STEP 6 → 10 YEAR CAGR FILTER
            if enable_10y:

                shortlisted_df = shortlisted_df[
                    shortlisted_df["10 Years CAGR"] >= avg_10y
                ]

            st.write("Rows after screening:", len(shortlisted_df))

            best_fund = shortlisted_df.sort_values(
                by="3 Years CAGR",
                ascending=False
            ).iloc[0]

            st.markdown(f"""
            <div style="
            background:linear-gradient(90deg,#0F5132,#198754);
            padding:20px;
            border-radius:15px;
            margin-bottom:20px;
            text-align:center;
            border:1px solid #28A745;
            ">
            <h2>🏆 Top Recommended Fund</h2>
            <h3>{best_fund['Scheme Name']}</h3>
            <p>
            3Y CAGR: {best_fund['3 Years CAGR']:.2f}% |
            Sharpe: {best_fund['Sharpe']:.2f} |
            Beta: {best_fund['Beta']:.2f}
            </p>
            </div>
            """, unsafe_allow_html=True)

            cagr_winner = shortlisted_df.loc[
                shortlisted_df["3 Years CAGR"].idxmax()
            ]

            sharpe_winner = shortlisted_df.loc[
                shortlisted_df["Sharpe"].idxmax()
            ]

            beta_winner = shortlisted_df.loc[
                shortlisted_df["Beta"].idxmin()
            ]

        # =================================================
        # FINAL SHORTLIST
        # =================================================

            st.subheader("Final Shortlisted Funds")

            st.dataframe(
                shortlisted_df[
                    [
                        "Scheme Name",
                        "Fund Size (Rs. Crs.)",
                        "3 Years CAGR",
                        "Sharpe",
                        "Beta",
                        "Risk Level"
                    ]
                ],
                use_container_width=True,
                height=300
            )

        # =====================================================
        # PORTFOLIO ALLOCATION PIE CHART
        # =====================================================

            st.subheader("Portfolio Allocation")

            avg_large = shortlisted_df["Large Cap %"].mean()
            avg_mid = shortlisted_df["Mid Cap %"].mean()
            avg_small = shortlisted_df["Small Cap %"].mean()
            avg_cash = shortlisted_df["Cash/Others %"].mean()

            fig_pie = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Large Cap",
                            "Mid Cap",
                            "Small Cap",
                            "Cash/Others"
                        ],
                        values=[
                            avg_large,
                            avg_mid,
                            avg_small,
                            avg_cash
                        ],
                        hole=0.4
                    )
                ]
            )

            fig_pie.update_layout(
                paper_bgcolor="#0E1117",
                font_color="white"
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )

        # =================================================
        # CAGR BAR CHART
        # =================================================

            st.subheader("Performance Comparison")

            chart_df = shortlisted_df.sort_values(
                by="3 Years CAGR",
                ascending=False
            )

            # 3Y CHART
            fig = px.bar(
                chart_df,
                x="Scheme Name",
                y="3 Years CAGR",
                color="3 Years CAGR",
                title="3Y CAGR"
            )

            fig.update_layout(
                xaxis_title="",
                yaxis_title="3Y CAGR",
                template="plotly_dark",
                height=300,
                yaxis_range=[0,20],
                coloraxis_showscale=False
            )

            st.plotly_chart(fig, use_container_width=True)


            # 5Y CHART
            fig_5 = px.bar(
                chart_df,
                x="Scheme Name",
                y="5 Years CAGR",
                color="5 Years CAGR",
                title="5Y CAGR"
            )

            fig_5.update_layout(
                xaxis_title="",
                yaxis_title="5Y CAGR",
                template="plotly_dark",
                height=300,
                yaxis_range=[0,20],
                coloraxis_showscale=False
            )

            st.plotly_chart(fig_5, use_container_width=True)


            # 10Y CHART
            fig_10 = px.bar(
                chart_df,
                x="Scheme Name",
                y="10 Years CAGR",
                color="10 Years CAGR",
                title="10Y CAGR"
            )

            fig_10.update_layout(
                xaxis_title="",
                yaxis_title="10Y CAGR",
                template="plotly_dark",
                height=300,
                yaxis_range=[0,20],
                coloraxis_showscale=False
            )

            st.plotly_chart(fig_10, use_container_width=True)
 
    # =================================================
    # SUMMARY CARDS
    # =================================================

            total_funds = len(clean_df)
            shortlisted_funds = len(shortlisted_df)

            best_cagr = shortlisted_df["3 Years CAGR"].max()
            lowest_beta = shortlisted_df["Beta"].min()

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div style="
                    background-color:#1C1F26;
                    padding:20px;
                    border-radius:15px;
                    border:1px solid #31333F;
                    text-align:center;
                ">
                    <h5 style="color:gray;">Total Funds</h5>
                    <h2 style="color:white;">{total_funds}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style="
                    background-color:#1C1F26;
                    padding:20px;
                    border-radius:15px;
                    border:1px solid #31333F;
                    text-align:center;
                ">
                    <h5 style="color:gray;">Shortlisted Funds</h5>
                    <h2 style="color:white;">{shortlisted_funds}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div style="
                    background-color:#1C1F26;
                    padding:20px;
                    border-radius:15px;
                    border:1px solid #31333F;
                    text-align:center;
                ">
                    <h5 style="color:gray;">Best 3Y CAGR</h5>
                    <h2 style="color:#00C853;">{best_cagr:.2f}%</h2>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div style="
                    background-color:#1C1F26;
                    padding:20px;
                    border-radius:15px;
                    border:1px solid #31333F;
                    text-align:center;
                ">
                    <h5 style="color:gray;">Lowest Beta</h5>
                    <h2 style="color:#FF4B4B;">{lowest_beta:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)

        # =================================================
        # DOWNLOAD BUTTON
        # =================================================

            csv = shortlisted_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Shortlisted Funds",
                data=csv,
                file_name="shortlisted_funds.csv",
                mime="text/csv"
            )

            with tab2:

                st.subheader("Compare Two Funds")

                fund1 = st.selectbox(
                    "Select Fund 1",
                    clean_df["Scheme Name"]
                )

                fund2 = st.selectbox(
                    "Select Fund 2",
                    clean_df["Scheme Name"],
                    index=1
                )

                fund1_data = clean_df[
                    clean_df["Scheme Name"] == fund1
                ].iloc[0]

                fund2_data = clean_df[
                    clean_df["Scheme Name"] == fund2
                ].iloc[0]
                comparison_df = pd.DataFrame({
                    "Metric": [
                        "Fund Size",
                        "3 Years CAGR",
                        "5 Years CAGR",
                        "10 Years CAGR",
                        "Sharpe Ratio",
                        "Beta"
                    ],
                    fund1: [
                        fund1_data["Fund Size (Rs. Crs.)"],
                        fund1_data["3 Years CAGR"],
                        fund1_data["5 Years CAGR"],
                        fund1_data["10 Years CAGR"],
                        fund1_data["Sharpe"],
                        fund1_data["Beta"]
                    ],
                    fund2: [
                        fund2_data["Fund Size (Rs. Crs.)"],
                        fund2_data["3 Years CAGR"],
                        fund2_data["5 Years CAGR"],
                        fund2_data["10 Years CAGR"],
                        fund2_data["Sharpe"],
                        fund2_data["Beta"]
                    ]
                })
                st.subheader("Comparison Table")

                st.dataframe(
                    comparison_df,
                    use_container_width=True
                )

                st.subheader("🏆 Fund Comparison Winners")

                col1, col2, col3 = st.columns(3)

                cagr_winner = (
                    fund1
                    if fund1_data["3 Years CAGR"] > fund2_data["3 Years CAGR"]
                    else fund2
                )

                sharpe_winner = (
                    fund1
                    if fund1_data["Sharpe"] > fund2_data["Sharpe"]
                    else fund2
                )

                beta_winner = (
                    fund1
                    if fund1_data["Beta"] < fund2_data["Beta"]
                    else fund2
                )

                with col1:
                    st.success(
                        f"""
                🏆 CAGR Winner

                {cagr_winner}

                {max(fund1_data['3 Years CAGR'], fund2_data['3 Years CAGR']):.2f}%
                """
                    )

                with col2:
                    st.success(
                        f"""
                🏆 Sharpe Winner

                {sharpe_winner}

                {max(fund1_data['Sharpe'], fund2_data['Sharpe']):.3f}
                """
                    )

                with col3:
                    st.success(
                        f"""
                🏆 Lower Risk Winner

                {beta_winner}

                Beta: {min(fund1_data['Beta'], fund2_data['Beta']):.2f}
                """
                    )


                