import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np # Included for robust category ordering

# --- Streamlit Page Config ---
st.set_page_config(page_title="Student Sleep & Stress Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Page Title ---
st.title("📊 Student Insomnia and Educational Outcomes Dashboard")

st.markdown("""
Explore the relationships between **sleep habits, stress levels, and academic performance** among students.
""")

# ==============================================
# 🔹 Key Metrics Section
# ==============================================
col1, col2, col3, col4 = st.columns(4)

# Clean numeric values for sleep hours
sleep_col = '4. On average, how many hours of sleep do you get on a typical day?'

# Try to extract numbers even if text contains words (e.g., "6 hours")
# NOTE: Using a simpler conversion assuming the string starts with the number
df[sleep_col] = df[sleep_col].astype(str).str.extract(r'(\d+\.?\d*)')
df[sleep_col] = pd.to_numeric(df[sleep_col], errors='coerce')

# Compute summary metrics safely
avg_sleep = df[sleep_col].mean()

# Handle categorical columns robustly (avoid KeyErrors)
stress_col = '14. How would you describe your stress levels related to academic workload?'
gpa_col = '15. How would you rate your overall academic performance (GPA or grades) in the past semester?'
gender_col = '2. What is your gender?'

avg_stress = df[stress_col].mode()[0] if not df[stress_col].empty else "N/A"
avg_gpa = df[gpa_col].mode()[0] if not df[gpa_col].empty else "N/A"
gender_ratio = df[gender_col].value_counts(normalize=True).idxmax() if not df[gender_col].empty else "N/A"

# Display metrics
col1.metric(
    label="🕒 Average Sleep Hours",
    value=f"{avg_sleep:.1f} hrs" if not pd.isna(avg_sleep) else "N/A",
    help="Average number of sleep hours reported by students",
    border=True
)

col2.metric(
    label="😰 Most Common Stress Level",
    value=avg_stress,
    help="Most frequently reported academic stress level",
    border=True
)

col3.metric(
    label="🎓 Typical Academic Performance",
    value=avg_gpa,
    help="Most commonly reported GPA/grade category",
    border=True
)

col4.metric(
    label="🚻 Majority Gender",
    value=gender_ratio,
    help="Gender with highest participation",
    border=True
)


# --- Show Data ---
with st.expander("🔍 View Dataset"):
    st.dataframe(df.head())

# ==============================================
# 1️⃣ Stacked Bar Chart – Stress Levels by Year of Study
# ==============================================
st.subheader("🎓 Academic Stress Levels by Year of Study")

stress_year_crosstab = pd.crosstab(
    df['1. What is your year of study?'],
    df['14. How would you describe your stress levels related to academic workload?'],
    normalize='index'
)

stress_year_crosstab = stress_year_crosstab.reset_index().melt(
    id_vars='1. What is your year of study?',
    var_name='Stress Level',
    value_name='Proportion'
)

fig1 = px.bar(
    stress_year_crosstab,
    x='1. What is your year of study?',
    y='Proportion',
    color='Stress Level',
    title='Academic Stress Levels by Year of Study',
    barmode='stack',
    color_discrete_sequence=px.colors.sequential.Sunset
)

fig1.update_layout(xaxis_title="Year of Study", yaxis_title="Proportion")
st.plotly_chart(fig1, use_container_width=True)

# ==============================================
# 2️⃣ Box Plot – Sleep Hours by Gender
# ==============================================
st.subheader("😴 Average Sleep Hours by Gender")

fig2 = px.box(
    df,
    x='2. What is your gender?',
    y='4. On average, how many hours of sleep do you get on a typical day?',
    color='2. What is your gender?',
    title='Average Sleep Hours by Gender',
    color_discrete_sequence=px.colors.sequential.Sunset
)

fig2.update_layout(xaxis_title="Gender", yaxis_title="Average Sleep Hours")
st.plotly_chart(fig2, use_container_width=True)

# ==============================================
# 3️⃣ Stacked Bar Chart – Sleep Quality by Year of Study
# ==============================================
st.subheader("🌙 Sleep Quality by Year of Study")
st.markdown("Proportion of students in each year of study reporting different levels of sleep quality.")

# 1. Create the normalized crosstab
sleep_quality_year_crosstab = pd.crosstab(
    df['1. What is your year of study?'], 
    df['6. How would you rate the overall quality of your sleep?'], 
    normalize='index'
)

# 2. Convert the wide crosstab format to a long format (melt) for Plotly Express
plot_data_sleep_year = sleep_quality_year_crosstab.reset_index()
plot_data_sleep_year = plot_data_sleep_year.melt(
    id_vars='1. What is your year of study?',
    var_name='Sleep Quality',
    value_name='Proportion'
)

# Define the category orders for consistent visualization
sleep_quality_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good']
# Ensure Year of Study is ordered logically (if possible, otherwise alphabetical)
year_of_study_order = sorted(plot_data_sleep_year['1. What is your year of study?'].unique())

# 3. Create the Plotly Stacked Bar Chart
fig_sleep_year = px.bar(
    plot_data_sleep_year,
    x='1. What is your year of study?',
    y='Proportion',
    color='Sleep Quality',
    barmode='stack', # Key for stacked bar chart
    category_orders={
        'Sleep Quality': sleep_quality_order,
        '1. What is your year of study?': year_of_study_order 
    },
    title='Sleep Quality by Year of Study',
    color_discrete_sequence=px.colors.sequential.Plasma_r # Color scheme similar to 'flare'
)

# 4. Update layout and display
fig_sleep_year.update_layout(
    xaxis_title="Year of Study", 
    yaxis_title="Proportion of Students",
    xaxis={'tickangle': 45}, # Rotate X-axis labels for readability
    legend_title_text='Sleep Quality'
)
st.plotly_chart(fig_sleep_year, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("✅ *Developed with Streamlit + Plotly | Dataset: Student Insomnia and Educational Outcomes*")
