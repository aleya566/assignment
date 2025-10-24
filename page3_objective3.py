import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# --- Streamlit Page Config ---
st.set_page_config(page_title="Impact of Sleep Issues on Academic Performance", layout="wide")

# --- Load Dataset ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Page Header ---
st.title("🧠 Impact of Sleep-Related Issues on Academic Performance")
st.markdown("""
Explore how **sleep difficulties, fatigue, and insufficient rest** influence students' **academic performance**.
""")

# --- Dataset Preview ---
with st.expander("🔍 View Dataset"):
    st.dataframe(df.head())

# =====================================================
# 1️⃣ Box Plot – Academic Performance vs Insufficient Sleep Impact
# =====================================================
st.subheader("📦 Academic Performance by Impact of Insufficient Sleep on Assignments")

# Map academic performance to numeric if needed
if '15. How would you rate your overall academic performance (GPA or grades) in the past semester?_numeric' not in df.columns:
    academic_performance_mapping = {
        'Poor': 1, 'Below Average': 2, 'Average': 3, 'Good': 4, 'Excellent': 5
    }
    df['15. How would you rate your overall academic performance (GPA or grades) in the past semester?_numeric'] = df[
        '15. How would you rate your overall academic performance (GPA or grades) in the past semester?'
    ].map(academic_performance_mapping)

# Define order for x-axis
impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']

fig1 = px.box(
    df,
    x='10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?',
    y='15. How would you rate your overall academic performance (GPA or grades) in the past semester?_numeric',
    color='10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?',
    category_orders={'10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?': impact_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    title='Academic Performance by Impact of Insufficient Sleep on Assignments'
)
fig1.update_layout(
    xaxis_title='Impact of Insufficient Sleep on Assignments',
    yaxis_title='Academic Performance (Numeric GPA/Grades)',
    xaxis_tickangle=45
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# 2️⃣ Heatmap – Concentration Difficulty vs Fatigue vs Academic Performance
# =====================================================
st.subheader("🔥 Average Academic Performance by Fatigue and Concentration Difficulty")

# Mapping categorical responses to numeric
concentration_mapping = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4}
fatigue_mapping = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4}

df['7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?_numeric'] = df[
    '7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?'
].map(concentration_mapping)
df['8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?_numeric'] = df[
    '8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?'
].map(fatigue_mapping)

# Ensure academic performance numeric exists
if '15. How would you rate your overall academic performance (GPA or grades) in the past semester?_numeric' not in df.columns:
    academic_performance_mapping = {
        'Poor': 1, 'Below Average': 2, 'Average': 3, 'Good': 4, 'Excellent': 5
    }
    df['15. How would you rate your overall academic performance (GPA or grades) in the past semester?_numeric'] = df[
        '15. How would you rate your overall academic performance (GPA or grades) in the past semester?'
    ].map(academic_performance_mapping)

# Create pivot table
heatmap_data = df.pivot_table(
    index='7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?_numeric',
    columns='8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?_numeric',
    values='15. How would you rate your overall academic performance (GPA or grades) in the past semester?_numeric',
    aggfunc='mean'
).reindex(list(concentration_mapping.values())).T.reindex(list(fatigue_mapping.values())).T

# Create interactive heatmap
fig2 = px.imshow(
    heatmap_data,
    text_auto=True,
    color_continuous_scale='Sunset',
    title='Average Academic Performance by Fatigue and Concentration Difficulty'
)
fig2.update_layout(
    xaxis_title='Fatigue Frequency (Numeric Scale)',
    yaxis_title='Concentration Difficulty (Numeric Scale)'
)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3️⃣ Violin Plot – Academic Performance by Difficulty Concentrating
# =====================================================
st.subheader("🎻 Distribution of Academic Performance by Difficulty Concentrating")

fig3 = px.violin(
    df,
    x='7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?',
    y='15. How would you rate your overall academic performance (GPA or grades) in the past semester?_numeric',
    color='7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?',
    box=True,
    points='all',
    category_orders={'7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?': ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']},
    color_discrete_sequence=px.colors.sequential.Sunset,
    title='Distribution of Academic Performance by Difficulty Concentrating Frequency'
)
fig3.update_layout(
    xaxis_title='Difficulty Concentrating Frequency',
    yaxis_title='Academic Performance (Numeric GPA/Grades)',
    xaxis_tickangle=45
)
st.plotly_chart(fig3, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("✅ *Developed with Streamlit + Plotly | Dataset: Student Insomnia and Educational Outcomes*")
