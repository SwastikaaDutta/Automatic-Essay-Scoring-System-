import streamlit as st
import textstat
from language_tool_python import LanguageTool
import time

# Page Configuration
st.set_page_config(page_title="EssayRater | AI Analysis", page_icon="📝", layout="wide")

# Custom CSS for Branding, Fonts, and Animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8fbff;
    }

    /* Professional Logo Styling */
    .logo-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 180px;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.1));
    }

    /* Fade-in Animation for Results */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .report-card {
        animation: fadeIn 0.8s ease-out;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* Buttons and Inputs */
    .stButton>button {
        background: linear-gradient(90deg, #1A4D8F, #4E6E81);
        color: white;
        border-radius: 12px;
        height: 3.5em;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(26, 77, 143, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# App Logo & Branding
# REPLACE THE URL BELOW WITH YOUR GITHUB IMAGE LINK
logo_url = "https://raw.githubusercontent.com/SwastikaaDutta/Automatic-Essay-Scoring-System-/refs/heads/main/logo-project.png" 
st.markdown(f'<img src="{logo_url}" class="logo-img">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1A4D8F;'>EssayRater</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Precision scoring for the next generation of writers.</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Scoring Config")
    total_marks = st.slider("Total Marks Weightage", 5, 100, 10)
    st.divider()
    st.caption("Developed by Swastika Dutta")

# Main Input Section
essay_text = st.text_area("Input Essay Content:", height=300, placeholder="Paste your text here to begin the AI evaluation...")

@st.cache_resource
def load_engine():
    return LanguageTool('en-US')

tool = load_engine()

if st.button("🚀 RUN AI ANALYSIS"):
    if not essay_text.strip():
        st.error("Please enter text to analyze.")
    else:
        with st.status("Analyzing essay structure...", expanded=True) as status:
            st.write("Checking grammar & punctuation...")
            matches = tool.check(essay_text)
            time.sleep(0.5)
            
            st.write("Calculating readability metrics...")
            readability = textstat.flesch_reading_ease(essay_text)
            time.sleep(0.5)
            
            st.write("Finalizing score...")
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # Scoring Logic
        error_count = len(matches)
        base_score = max(0, 100 - (error_count * 2.5))
        final_grade = round((base_score / 100) * total_marks, 2)
        word_count = textstat.lexicon_count(essay_text)

        # Results Display with Animation Wrapper
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Awarded Score", f"{final_grade}/{total_marks}")
        m2.metric("Grammar Issues", error_count)
        m3.metric("Word Count", word_count)
        m4.metric("Reading Ease", f"{readability}%")

        st.progress(int(base_score))

        t1, t2 = st.tabs(["📝 Detailed Feedback", "📈 Analytics"])
        
        with t1:
            if error_count == 0:
                st.balloons()
                st.success("Flawless writing! Your grammar is perfect.")
            else:
                for m in matches[:8]:
                    st.error(f"**Issue:** {m.message}")
                    st.caption(f"Suggestion: {m.replacements[:3]}")

        with t2:
            st.write(f"**Sentence Count:** {textstat.sentence_count(essay_text)}")
            st.write(f"**Estimated Grade Level:** {textstat.flesch_kincaid_grade(essay_text)}")
            st.info("Tip: Aim for a Readability score between 60-70 for general audiences.")

        st.markdown('</div>', unsafe_allow_html=True)
