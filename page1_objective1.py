# ==============================================
# 📘 OBJECTIVE 1 – Exploration: Who is affected?
# ==============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np  # For sorting categories

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
Explore how **sleep habits** and **academic stress** vary among students by year of study and gender.
This section aims to identify **who is most affected** by stress and poor sleep quality.
""")

# ==============================================
# 🔹 Overview of Student Sleep, Stress, and Demographics
# ==============================================
st.subheader("🧭 Overview of Student Sleep, Stress, and Demographics")

st.markdown("""
This section provides a quick overview of the dataset, summarizing key indicators such as 
average sleep duration, common stress levels, overall academic performance, and gender distribution.  
These metrics give context for understanding **who is most affected** by stress and sleep-related issues.
""")

# --- Key Metrics Section ---
col1, col2, col3, col4 = st.columns(4)

# Clean numeric values for sleep hours
sleep_col = '4. On average, how many hours of sleep do you get on a typical day?'
df[sleep_col] = df[sleep_col].astype(str).str.extract(r'(\d+\.?\d*)')
df[sleep_col] = pd.to_numeric(df[sleep_col], errors='coerce')

# Define columns
stress_col = '14. How would you describe your stress levels related to academic workload?'
gpa_col = '15. How would you rate your overall academic performance (GPA or grades) in the past semester?'
gender_col = '2. What is your gender?'

# Compute summary metrics
avg_sleep = df[sleep_col].mean()
avg_stress = df[stress_col].mode()[0] if not df[stress_col].empty else "N/A"
avg_gpa = df[gpa_col].mode()[0] if not df[gpa_col].empty else "N/A"
gender_ratio = df[gender_col].value_counts(normalize=True).idxmax() if not df[gender_col].empty else "N/A"

# Display metrics
col1.metric("🕒 Avg. Sleep Hours", f"{avg_sleep:.1f} hrs" if not pd.isna(avg_sleep) else "N/A")
col2.metric("😰 Common Stress Level", avg_stress)
col3.metric("🎓 Typical GPA Category", avg_gpa)
col4.metric("🚻 Majority Gender", gender_ratio)

# --- Transition Caption ---
st.markdown("""
---
These summary indicators highlight key aspects of students’ overall well-being.  
The following visualizations further **explore how stress levels and sleep patterns differ** across academic years and genders — revealing **who is most affected** by insomnia-related challenges.
""")

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

sleep_quality_year_crosstab = pd.crosstab(
    df['1. What is your year of study?'], 
    df['6. How would you rate the overall quality of your sleep?'], 
    normalize='index'
)

plot_data_sleep_year = sleep_quality_year_crosstab.reset_index().melt(
    id_vars='1. What is your year of study?',
    var_name='Sleep Quality',
    value_name='Proportion'
)

sleep_quality_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good']
year_of_study_order = sorted(plot_data_sleep_year['1. What is your year of study?'].unique())

fig_sleep_year = px.bar(
    plot_data_sleep_year,
    x='1. What is your year of study?',
    y='Proportion',
    color='Sleep Quality',
    barmode='stack',
    category_orders={
        'Sleep Quality': sleep_quality_order,
        '1. What is your year of study?': year_of_study_order 
    },
    title='Sleep Quality by Year of Study',
    color_discrete_sequence=px.colors.sequential.Plasma_r
)

fig_sleep_year.update_layout(
    xaxis_title="Year of Study", 
    yaxis_title="Proportion of Students",
    xaxis={'tickangle': 45},
    legend_title_text='Sleep Quality'
)
st.plotly_chart(fig_sleep_year, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("✅ *Developed with Streamlit + Plotly | Dataset: Student Insomnia and Educational Outcomes*")
