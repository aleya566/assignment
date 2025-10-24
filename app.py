import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION AND THEME (Crucial for the appearance) ---
# Set the page configuration for a wide layout and a dark theme if not already set globally
st.set_page_config(
    page_title="Arts Faculty Data Visualization",
    layout="wide",
    initial_sidebar_state="expanded",
)

# NOTE: The dark theme in your image is typically achieved by setting the
# 'theme.base' to 'dark' in the .streamlit/config.toml file,
# OR by the user setting their Streamlit app to dark mode.
# We will use st.markdown to try and inject some dark mode styling for the metrics.

# --- Data Loading (Using the original logic as a placeholder) ---
@st.cache_data
def load_data():
    """Loads a placeholder dataset or your actual Arts dataset."""
    # Since your original code was for a *different* dataset, I'll use a placeholder
    # that mimics the structure implied by your screenshot's column names.
    # Replace this URL with your actual "Arts Faculty" dataset URL if you have it.
    try:
        url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
        df = pd.read_csv(url)
        # Rename columns to match the general feel of the screenshot's data
        df.rename(columns={
            '1. What is your year of study?': 'Academic Year in EU',
            '2. What is your gender?': 'Gender',
            '1. What is your year of study?': 'Faculty Program',
            # Add more renames if you use the actual Arts data
        }, inplace=True)
        # Filter for a hypothetical 'Arts' faculty if possible, or just use the first few columns
        df_display = df.iloc[:, :7]
    except Exception:
        # Create a dummy DataFrame if the URL fails or for demonstration
        data = {
            'Timestamp': pd.to_datetime(['1/25/2016 14:26', '1/25/2016 14:38', '1/25/2016 14:40', '1/25/2016 14:43', '1/25/2016 14:45']),
            'Gender': ['Male', 'Female', 'Male', 'Male', 'Female'],
            'Faculty Program': ['Arts', 'B.A. in English', 'Arts', 'B.A. in English', 'B.A. in English'],
            'Academic Year in EU': ['3rd Year', '4th Year', '3rd Year', '3rd Year', '4th Year'],
            'Masters Academic Year in EU': ['None', 'None', 'None', 'None', 'None'],
            'H.S.C or Equivalent study medium': ['Bangla Medium', 'Bangla Medium', 'Bangla Medium', 'Bangla Medium', 'Bangla Medium'],
            'H.S.C.(GPA)': [4.88, 4.56, 4.25, 3.38, 5.0]
        }
        df_display = pd.DataFrame(data)

    return df_display

df = load_data()

# --- SIDEBAR FOR NAVIGATION ---
with st.sidebar:
    st.subheader("Menu")
    # This structure mimics the multi-page app look, even if it's a single page file
    st.page_link("app.py", label="Homepage", icon="🏠")
    st.page_link("app.py", label="Pencapaian Akademik Pela...", icon="📊")
    st.markdown("---") # Separator
    st.markdown("More About Float A...")
    st.markdown("Data Structures and...")


# --- METRIC CARDS SECTION (PLOs) ---
# Use st.columns to lay out the metrics side-by-side
st.markdown("""
<style>
.metric-card {
    background-color: #262730; /* Darker background for the card */
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
}
.metric-value {
    font-size: 3.5em; /* Large value text */
    font-weight: bold;
    color: #4CAF50; /* Green/primary color */
}
.metric-label {
    font-size: 1.2em; /* Label text size */
    margin-top: 5px;
    color: #AFAFB2; /* Lighter text color */
}
</style>
""", unsafe_allow_html=True)

# Define columns for the four metrics
col_plo2, col_plo3, col_plo4, col_plo5 = st.columns(4)

# Use st.metric for simplicity, but wrap it in an HTML block to force styling
# Alternatively, you can use raw HTML/Markdown to create the full custom card look:
with col_plo2:
    st.markdown('<div class="metric-card"><div class="metric-label">PLO 2</div><div class="metric-value">3.3</div></div>', unsafe_allow_html=True)
    # st.metric(label="PLO 2", value="3.3") # The default st.metric doesn't look like the image

with col_plo3:
    st.markdown('<div class="metric-card"><div class="metric-label">PLO 3</div><div class="metric-value">3.5</div></div>', unsafe_allow_html=True)

with col_plo4:
    st.markdown('<div class="metric-card"><div class="metric-label">PLO 4</div><div class="metric-value">4.0</div></div>', unsafe_allow_html=True)

with col_plo5:
    st.markdown('<div class="metric-card"><div class="metric-label">PLO 5</div><div class="metric-value">4.3</div></div>', unsafe_allow_html=True)

st.markdown("---")

# --- MAIN TITLE AND DESCRIPTION ---
st.header('Arts Faculty Data Visualization')
st.markdown(
    'This dashboard presents key distributions from the Arts Faculty dataset using Plotly.'
)

# --- DATA PREVIEW SECTION ---
st.subheader('Data Preview')
st.dataframe(df) # Display the DataFrame

# --- VISUALIZATION HEADINGS (Placeholder for your charts) ---
st.markdown("## 1. Distribution of Arts Programs") # Use markdown headings for a larger font
st.markdown("## 2. Academic Year Distribution") # Use markdown headings for a larger font

# NOTE: The actual Plotly charts you had previously would go here.
# For example:
# st.write("Placeholder for your Plotly chart 1 here.")
# st.write("Placeholder for your Plotly chart 2 here.")

# --- END OF APP ---
