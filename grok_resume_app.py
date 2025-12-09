import streamlit as st
import PyPDF2
import io
import nltk
import plotly.graph_objects as go
import re
from collections import Counter

# Download NLTK data (needed for keyword extraction)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Grok Resume Tailorer",
    page_icon="🎯",
    layout="wide"
)

# ==================== DARK MODE CSS ====================
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2a9df4;
    }
    h1 {
        color: #00d4ff;
    }
    h2, h3 {
        color: #4dd4ff;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_keywords(text):
    """Extract meaningful keywords from text using NLTK"""
    # Convert to lowercase and tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.isalpha() and word not in stop_words and len(word) > 2]
    
    return keywords

def calculate_ats_keyword_score(resume_text, jd_text):
    """Calculate keyword match percentage between resume and JD"""
    resume_keywords = set(extract_keywords(resume_text))
    jd_keywords = set(extract_keywords(jd_text))
    
    if len(jd_keywords) == 0:
        return 0
    
    # Calculate percentage of JD keywords found in resume
    matched_keywords = resume_keywords.intersection(jd_keywords)
    score = (len(matched_keywords) / len(jd_keywords)) * 100
    
    return min(score, 100)  # Cap at 100

# ==================== MOCK GROK FUNCTIONS ====================
# 🔑 TODO: Replace these with real Grok API calls
# Your Grok API key will go here: GROK_API_KEY = "your-api-key-here"

def mock_grok_suggestions(resume_text, jd_text):
    """
    Mock function to generate tailoring suggestions
    
    🔑 REAL IMPLEMENTATION:
    - Use Grok API to analyze resume vs JD
    - Prompt: "Compare this resume with the job description and provide 5 ranked suggestions..."
    - Return structured suggestions with impact ranking
    """
    suggestions = [
        {
            "rank": 1,
            "suggestion": "Add specific metrics to quantify your achievements",
            "explanation": "The JD emphasizes results-driven candidates. Adding percentages, dollar amounts, or scale (e.g., 'Increased revenue by 35%') will significantly boost your ATS score and catch recruiters' attention."
        },
        {
            "rank": 2,
            "suggestion": "Mirror exact keywords from the job description",
            "explanation": "ATS systems scan for exact keyword matches. Incorporate phrases like those found in the JD (e.g., if JD says 'stakeholder management', use that exact phrase rather than 'working with partners')."
        },
        {
            "rank": 3,
            "suggestion": "Restructure experience bullets to lead with action verbs",
            "explanation": "Start each bullet with strong verbs like 'Orchestrated', 'Spearheaded', 'Optimized'. This creates immediate impact and aligns with the JD's dynamic language."
        },
        {
            "rank": 4,
            "suggestion": "Add a skills section matching JD requirements",
            "explanation": "Create a dedicated skills section featuring technical and soft skills mentioned in the JD. This provides easy scanning for both ATS and human reviewers."
        },
        {
            "rank": 5,
            "suggestion": "Tailor your summary/objective to match the role",
            "explanation": "Your opening statement should mirror the job title and key requirements from the JD. This immediately signals you're a relevant candidate to the ATS algorithm."
        }
    ]
    return suggestions

def mock_grok_tailored_resume(resume_text, jd_text):
    """
    Mock function to generate tailored resume
    
    🔑 REAL IMPLEMENTATION:
    - Use Grok API with prompt: "Rewrite this resume to align with the job description..."
    - Emphasize: "Keep all facts 100% truthful, only rephrase and reorganize"
    - Request natural keyword integration
    """
    # This is a simplified mock - real version would intelligently rewrite
    tailored = f"""TAILORED RESUME (Mock Version)
    
📌 PROFESSIONAL SUMMARY
Results-driven professional with proven expertise in the key areas highlighted in your target role. Demonstrated success in stakeholder management, cross-functional collaboration, and data-driven decision making. Ready to bring quantifiable impact to your next position.

💼 PROFESSIONAL EXPERIENCE

Senior Analyst | Tech Company Inc. | 2021 - Present
• Spearheaded process optimization initiatives resulting in 35% efficiency improvement and $250K annual cost savings
• Orchestrated stakeholder management across 5 departments, aligning strategic objectives with business outcomes
• Leveraged advanced analytics and data visualization to drive executive decision-making
• Mentored team of 4 junior analysts, improving team productivity by 28%

Business Analyst | Solutions Corp | 2019 - 2021
• Optimized workflow processes through requirements gathering and agile methodologies
• Collaborated with cross-functional teams to deliver 12+ projects on time and under budget
• Implemented dashboard reporting system increasing operational visibility by 40%

🎓 EDUCATION
Bachelor of Science in Business Analytics | State University | 2019
• Relevant Coursework: Data Analytics, Business Intelligence, Statistics

🛠️ SKILLS
Technical: SQL, Python, Tableau, Excel (Advanced), Power BI, Data Analysis
Soft Skills: Stakeholder Management, Cross-functional Collaboration, Strategic Planning, Problem Solving

📊 CERTIFICATIONS
• Certified Business Analysis Professional (CBAP)
• Project Management Professional (PMP)

---
✅ This resume has been tailored to match your job description with naturally integrated keywords while maintaining 100% factual accuracy.
"""
    return tailored

def mock_ats_scores(is_tailored=False):
    """
    Mock function for 6 ATS scores (keyword score is calculated separately)
    
    🔑 REAL IMPLEMENTATION:
    - Use Grok API to analyze resume quality
    - Prompt: "Analyze this resume and rate it on: Skills Hit, Experience Depth, etc."
    - Return scores 0-100 for each category
    """
    if is_tailored:
        return {
            "Skills Hit": 92,
            "Experience Depth": 88,
            "Quantitative Impact": 95,
            "Title Fit": 90,
            "Education Match": 85,
            "Parseability": 93
        }
    else:
        return {
            "Skills Hit": 62,
            "Experience Depth": 68,
            "Quantitative Impact": 45,
            "Title Fit": 58,
            "Education Match": 75,
            "Parseability": 72
        }

# ==================== MAIN APP ====================

st.title("🎯 Grok Resume Tailorer")
st.markdown("### Transform your resume to match any job description using AI")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
with col2:
    st.markdown("#### 📋 Paste Job Description")
    job_description = st.text_area("Enter the full job description", height=200, 
                                   placeholder="Paste the complete job posting here...")

st.markdown("---")

# Analyze button
if st.button("🚀 Analyze & Tailor Resume", use_container_width=True):
    
    if uploaded_file is None:
        st.error("❌ Please upload a resume PDF first!")
    elif not job_description.strip():
        st.error("❌ Please paste a job description!")
    else:
        with st.spinner("🤖 AI is analyzing and tailoring your resume..."):
            
            # Extract resume text
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Store in session state
            st.session_state['resume_text'] = resume_text
            st.session_state['jd_text'] = job_description
            
            # Generate suggestions
            suggestions = mock_grok_suggestions(resume_text, job_description)
            st.session_state['suggestions'] = suggestions
            
            # Generate tailored resume
            tailored_resume = mock_grok_tailored_resume(resume_text, job_description)
            st.session_state['tailored_resume'] = tailored_resume
            
            # Calculate ATS scores
            # Original scores
            original_keyword_score = calculate_ats_keyword_score(resume_text, job_description)
            original_other_scores = mock_ats_scores(is_tailored=False)
            
            # Tailored scores
            tailored_keyword_score = calculate_ats_keyword_score(tailored_resume, job_description)
            tailored_other_scores = mock_ats_scores(is_tailored=True)
            
            st.session_state['original_scores'] = {
                "Keyword Match": original_keyword_score,
                **original_other_scores
            }
            st.session_state['tailored_scores'] = {
                "Keyword Match": tailored_keyword_score,
                **tailored_other_scores
            }
        
        st.success("✅ Analysis complete!")

# Display results if they exist
if 'suggestions' in st.session_state:
    
    st.markdown("---")
    st.markdown("## 💡 Top 5 Tailoring Suggestions")
    
    for sug in st.session_state['suggestions']:
        with st.expander(f"🏆 #{sug['rank']} - {sug['suggestion']}", expanded=(sug['rank']==1)):
            st.markdown(f"**Why this matters:** {sug['explanation']}")
    
    st.markdown("---")
    st.markdown("## 📊 ATS Score Comparison")
    
    # Create radar chart
    categories = list(st.session_state['original_scores'].keys())
    original_values = list(st.session_state['original_scores'].values())
    tailored_values = list(st.session_state['tailored_scores'].values())
    average_values = [70] * len(categories)  # Industry average
    
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatterpolar(
        r=original_values,
        theta=categories,
        fill='toself',
        name='Current Resume',
        line=dict(color='#ff4444', width=2),
        fillcolor='rgba(255, 68, 68, 0.2)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=tailored_values,
        theta=categories,
        fill='toself',
        name='Tailored Resume',
        line=dict(color='#00d4ff', width=2),
        fillcolor='rgba(0, 212, 255, 0.2)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=average_values,
        theta=categories,
        fill=None,
        name='Industry Average',
        line=dict(color='#888888', width=2, dash='dot')
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#0e1117',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#333333',
                tickfont=dict(color='#ffffff')
            ),
            angularaxis=dict(
                gridcolor='#333333',
                tickfont=dict(color='#ffffff', size=12)
            )
        ),
        showlegend=True,
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font=dict(color='#ffffff'),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Score summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_original = sum(original_values) / len(original_values)
        st.metric("🔴 Current Score", f"{avg_original:.1f}%")
    
    with col2:
        avg_tailored = sum(tailored_values) / len(tailored_values)
        improvement = avg_tailored - avg_original
        st.metric("🔵 Tailored Score", f"{avg_tailored:.1f}%", 
                 delta=f"+{improvement:.1f}%")
    
    with col3:
        st.metric("⚪ Industry Average", "70.0%")
    
    st.markdown("---")
    st.markdown("## ✨ Your Tailored Resume")
    
    st.text_area("Preview", st.session_state['tailored_resume'], 
                height=400, disabled=True)
    
    # Download button
    st.download_button(
        label="📥 Download Tailored Resume",
        data=st.session_state['tailored_resume'],
        file_name="tailored_resume.txt",
        mime="text/plain",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666666;'>
    <p>🤖 Powered by AI | Built with Streamlit | Made for Job Seekers</p>
    <p style='font-size: 12px;'>💡 Tip: Always review and personalize your tailored resume before sending!</p>
</div>
""", unsafe_allow_html=True)