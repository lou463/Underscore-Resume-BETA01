import streamlit as st
import PyPDF2
import plotly.graph_objects as go
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download once
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# ==================== PAGE & STYLE ====================
st.set_page_config(page_title="Grok Resume Tailorer", layout="wide")
st.markdown("""
<style>
    .main {background-color: #0e1117; color: white;}
    .stButton>button {background-color: #1f77b4; color: white; border-radius: 12px; padding: 12px 40px; font-size: 18px; font-weight: bold;}
    .stButton>button:hover {background-color: #2a9df4;}
    h1, h2, h3 {color: #00d4ff;}
    .stExpander {background-color: #1a1a2e; border: 1px solid #333;}
</style>
""", unsafe_allow_html=True)

st.title("🎯 Grok Resume Tailorer")
st.markdown("### Upload your resume + paste any job → get ranked suggestions, tailored version & dark ATS spider chart")

# ==================== FUNCTIONS ====================
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def mock_suggestions():
    return [
        {"rank": 1, "suggestion": "Add A/B testing & funnel optimization keywords", "why": "Appears 6 times in JD — huge ATS boost"},
        {"rank": 2, "suggestion": "Quantify community value at TRAME", "why": "JD wants 'high-value member growth' — add '0→1000+ members'"},
        {"rank": 3, "suggestion": "Shorten early sales roles", "why": "Recruiters ignore anything before 2023"},
        {"rank": 4, "suggestion": "Categorize Skills section", "why": "ATS parses better, humans scan faster"},
        {"rank": 5, "suggestion": "Fix date formats", "why": "Prevents parsing errors"}
    ]

def mock_tailored():
    return """LUIS LANDEROS
Head of Growth | 11× DAU & 30× Volume Growth via User Acquisition & Funnel Optimization

• Current: 11× DAU (9→100+, peaks 212) and 30× volume ($112k→$3.4M) in 7 months
• Built 0→1 ambassador & referral systems driving 35–40% of all growth
• Cut CAC 45% and lifted Week-1 retention 2.2× via AI-powered onboarding
• Daily AI force-multiplier (copy, creatives, A/B testing, funnel optimization)

HEAD OF GROWTH (Remote) | April 2025 – Present
Vyper – Privacy-first investment platform
• Led user acquisition and funnel optimization to 11× DAU and 30× platform volume
• Designed ambassador + referral engine driving 35–40% of new users and deposits
• Reduced CAC 45% and lifted Week-1 retention 2.2× via onboarding redesign and A/B testing
• Integrated AI workflows accelerating experimentation velocity 3–4×
• Partnered with 45+ tier-1 creators and communities

[Full tailored resume continues...]
"""

def ats_scores():
    return [88, 92, 96, 99, 94, 85, 98]  # Real version will calculate from text

# ==================== UI ====================
col1, col2 = st.columns(2)
with col1:
    resume = st.file_uploader("📄 Upload Resume PDF", type="pdf")
with col2:
    jd = st.text_area("📋 Paste Job Description", height=180)

if st.button("🚀 Analyze & Tailor Resume", use_container_width=True):
    if not resume:
        st.error("Please upload your resume PDF")
    elif not jd.strip():
        st.error("Please paste a job description")
    else:
        with st.spinner("Grok is analyzing..."):
            text = extract_text(resume)
            
            # Show results
            st.success("Done! Here are your results:")
            
            # Suggestions
            st.subheader("Top 5 Ranked Suggestions")
            for s in mock_suggestions():
                with st.expander(f"#{s['rank']} — {s['suggestion']}"):
                    st.write(s['why'])
            
            # Tailored Resume
            st.subheader("Your Tailored Resume")
            tailored = mock_tailored()
            st.download_button("📥 Download Tailored Resume", tailored, "Tailored_Resume.txt")
            st.text_area("Copy-paste ready", tailored, height=500)
            
            # Spider Chart
            st.subheader("Interactive ATS Spider Chart")
            scores = ats_scores()
            labels = ["Keyword Match", "Skills", "Experience", "Quant Impact", "Title Fit", "Education", "Parseability"]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=scores, theta=labels, fill='toself', name='Your Resume', line_color='#00d4ff'))
            fig.add_trace(go.Scatterpolar(r=[70]*7, theta=labels, name='Average Applicant', line=dict(color='gray', dash='dot')))
            fig.update_layout(polar=dict(radialaxis=dict(range=[0,100]), bgcolor='#0e1117'),
                              paper_bgcolor='#0e1117', font_color="white", title="Your ATS Score vs Average")
            st.plotly_chart(fig, use_container_width=True)
            
            st.success("Overall ATS Score: 93/100 — Top 3% of applicants!")
            st.balloons()

else:
    st.info("Upload your resume + paste any job description to start")

st.caption("Built with ❤️ using Streamlit • Mock mode (real Grok coming soon)")
