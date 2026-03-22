import streamlit as st
import textstat
from language_tool_python import LanguageTool

# Initialize grammar tool (This is free and works offline/online)
tool = LanguageTool('en-US')

st.set_page_config(page_title="AI Essay Scorer", layout="centered")

st.title("📝 Automatic Essay Scoring System")
st.markdown("Enter your essay below to get an instant analysis on grammar, readability, and length.")

essay_text = st.text_area("Paste your essay here:", height=300)

if st.button("Analyze Essay"):
    if essay_text.strip() == "":
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Analyzing..."):
            # 1. Grammar & Punctuation Check
            matches = tool.check(essay_text)
            grammar_score = max(0, 100 - len(matches)) # Simple logic: deduct 1 point per error
            
            # 2. Readability (Flesch-Kincaid)
            readability = textstat.flesch_reading_ease(essay_text)
            
            # 3. Word Count / Structure
            word_count = textstat.lexicon_count(essay_text, removepunct=True)
            
            # Display Results
            st.divider()
            col1, col2, col3 = st.columns(3)
            
            col1.metric("Grammar Score", f"{grammar_score}/100")
            col2.metric("Readability", f"{readability}")
            col3.metric("Word Count", word_count)
            
            # Detailed Feedback
            st.subheader("Analysis Breakdown")
            
            with st.expander("Grammar & Punctuation Details"):
                if len(matches) == 0:
                    st.success("No major errors found!")
                else:
                    for match in matches[:10]: # Show top 10 errors
                        st.write(f"- {match.message} (Context: '...{match.context[-20:]}...')")
            
            with st.expander("Readability Guide"):
                st.write("Score > 60: Standard/Easy to read.")
                st.write("Score < 50: Fairly difficult (College level).")
