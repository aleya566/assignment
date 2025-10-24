import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Survey Dashboard", layout="wide")

# --- Load dataset ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Page imports ---
home = st.Page("page1_objective1.py", title="Objective 1 – Sleep Distribution", icon=":material/bar_chart:", default=True)
page2 = st.Page("page2_objective2.py", title="Objective 2 – Lifestyle Impact", icon=":material/self_improvement:")
page3 = st.Page("page3_objective3.py", title="Objective 3 – Academic Performance", icon=":material/school:")

# --- Navigation setup ---
pg = st.navigation({
    "Student Survey Menu": [home, page2, page3]
})

pg.run()
