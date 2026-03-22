import streamlit as st
import textstat
from language_tool_python import LanguageTool

# Page Configuration
st.set_page_config(page_title="AI Essay Scorer Pro", page_icon="📝", layout="wide")

# Custom CSS for a better UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #4E6E81;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #4E6E81;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2F4858;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Inputs
with st.sidebar:
    st.header("⚙️ Settings")
    total_marks = st.number_input("Maximum Marks for Essay", min_value=1, max_value=100, value=10)
    st.info("The system will calculate the final score based on this total.")

# Main UI
st.title("🚀 Smart Essay Analyzer")
st.caption("AI-powered evaluation for Grammar, Readability, and Structure.")

# Input Area
essay_text = st.text_area("Drop your essay content here...", height=300, placeholder="Start typing or paste your essay...")

# Grammar Tool Initialization (Cached to save time)
@st.cache_resource
def get_tool():
    return LanguageTool('en-US')

tool = get_tool()

if st.button("✨ Evaluate My Essay"):
    if not essay_text.strip():
        st.error("Please provide some text to analyze.")
    else:
        with st.spinner("🤖 AI is reading your essay..."):
            # 1. Logic Calculations
            matches = tool.check(essay_text)
            error_count = len(matches)
            
            # Scoring Logic: 
            # We calculate a % score based on errors and word count, 
            # then map it to your 'total_marks'.
            base_score = max(0, 100 - (error_count * 2)) # Deduction per error
            final_grade = round((base_score / 100) * total_marks, 1)
            
            readability = textstat.flesch_reading_ease(essay_text)
            word_count = textstat.lexicon_count(essay_text)
            
            # UI Presentation: Results Section
            st.success("Analysis Complete!")
            
            # Top Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Final Score", f"{final_grade} / {total_marks}")
            m2.metric("Grammar Errors", error_count, delta=-error_count, delta_color="inverse")
            m3.metric("Word Count", word_count)
            m4.metric("Readability", f"{readability}%")

            # Progress Bar for Visual Appeal
            st.write(f"**Overall Performance: {base_score}%**")
            st.progress(base_score / 100)

            # Detailed Tabs
            tab1, tab2 = st.tabs(["🔍 Grammar Report", "📊 Stylistic Insights"])
            
            with tab1:
                if error_count == 0:
                    st.balloons()
                    st.success("Perfect! No grammar issues detected.")
                else:
                    st.warning(f"Found {error_count} areas for improvement:")
                    for i, match in enumerate(matches[:15]): # Limit to top 15
                        st.markdown(f"**{i+1}.** {match.message}")
                        st.caption(f"Context: ...{match.context}...")

            with tab2:
                st.write("### Structure Breakdown")
                if word_count < 100:
                    st.info("Short Essay: Focus on expanding your arguments.")
                elif word_count > 500:
                    st.info("Comprehensive Essay: Good depth of coverage.")
                
                st.write(f"- **Sentences:** {textstat.sentence_count(essay_text)}")
                st.write(f"- **Average Grade Level:** {textstat.flesch_kincaid_grade(essay_text)}")
