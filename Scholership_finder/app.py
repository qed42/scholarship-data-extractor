import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

# Configuration
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY', 'your_key_here')
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load and prepare data
@st.cache_data
def load_scholarships():
    try:
        df = pd.read_csv("scholarships_data.csv", quotechar='"', quoting=1)
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df.rename(columns=lambda x: x.strip(), inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Convert CSV to RAG context
def create_rag_context(df):
    context = "Scholarship Database:\n\n"
    for _, row in df.iterrows():
        context += f"""Scholarship Name: {row['Scholarship Name']}
Eligibility: {row['Eligibility']}
Deadline: {row['Deadline']}
Link: {row['Link']}\n\n"""
    return context

# Initialize Gemini model
def get_rag_model():
    return genai.GenerativeModel('gemini-1.5-pro')

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    /* Custom color for results */
    .stMarkdown p, .stMarkdown ul, .stMarkdown ol {
        color: rgb(1, 27, 29); /* Custom color for results */
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app
def main():
    # Load custom CSS
    load_css()

    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1 style="color: #2c3e50; font-size: 3rem;">🎓 AI Scholarship Advisor</h1>
        <p style="color: #34495e; font-size: 1.2rem;">Find the best scholarships tailored just for you!</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data and create RAG context
    df = load_scholarships()
    rag_context = create_rag_context(df)

    # User input form
    with st.form("profile_form"):
        st.markdown("### 📝 Student Profile")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 16, 50, 20)
            citizenship = st.selectbox("Citizenship", ["India", "Other"])
            income = st.number_input("Annual Family Income (₹)", 0, 10000000, 300000)
        with col2:
            education = st.selectbox("Education Level", 
                                   ["High School", "Undergraduate", "Postgraduate", "PhD"])
            category = st.selectbox("Category", 
                                  ["General", "OBC", "SC", "ST", "EWS", "Minority"])
        
        submitted = st.form_submit_button("🚀 Get Recommendations")

    if submitted:
        # Create user profile
        user_profile = f"""
        Student Profile:
        - Age: {age}
        - Citizenship: {citizenship}
        - Annual Income: ₹{income}
        - Education Level: {education}
        - Category: {category}
        """

        # Generate response using RAG
        model = get_rag_model()
        prompt = f"""
        {rag_context}

        {user_profile}

        Task: 
        1. Analyze the student profile against all scholarships
        2. Identify top 5 most relevant scholarships with priority order
        3. For each scholarship:
           - List matching eligibility criteria
           - Explain why it's a good match
           - Provide direct application link
        4. Format response with markdown headers and bullet points

        Important: 
        - Be specific about eligibility matches
        - Highlight deadlines if available
        - Never invent scholarships not in the database
        """

        with st.spinner("🔍 Analyzing 50+ scholarships..."):
            response = model.generate_content(
                prompt,
                generation_config=GenerationConfig(
                    temperature=0.3,
                    top_p=0.95,
                    max_output_tokens=2000
                )
            )

        # Display recommendations
        st.markdown("### 🎉 Personalized Recommendations")
        st.markdown(response.text)

        # Show raw data for transparency
        with st.expander("📊 View Full Scholarship Database"):
            st.dataframe(df)

if __name__ == "__main__":
    main()