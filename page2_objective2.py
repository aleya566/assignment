import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np

# --- Streamlit Page Config ---
st.set_page_config(page_title="Lifestyle & Sleep Analysis", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Page Title ---
st.title("📊 Analysis Dashboard: Lifestyle Behaviors and Their Influence on Sleep Quality")

st.markdown("""
Analyze how **caffeine consumption**, **physical activity**, and **device usage** influence students' **sleep quality** and **sleep duration**.
""")

# ==============================================
# 🔹 Key Metrics Section
# ==============================================
col1, col2, col3, col4 = st.columns(4)

sleep_quality_col = '6. How would you rate the overall quality of your sleep?'
caffeine_col = '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?'
device_col = '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?'
exercise_col = '13. How often do you engage in physical activity or exercise?'

most_common_sleep_quality = df[sleep_quality_col].mode()[0] if not df[sleep_quality_col].empty else "N/A"
most_common_caffeine = df[caffeine_col].mode()[0] if not df[caffeine_col].empty else "N/A"
most_common_device = df[device_col].mode()[0] if not df[device_col].empty else "N/A"
most_common_exercise = df[exercise_col].mode()[0] if not df[exercise_col].empty else "N/A"

col1.metric("💤 Most Common Sleep Quality", most_common_sleep_quality)
col2.metric("☕ Typical Caffeine Use", most_common_caffeine)
col3.metric("📱 Typical Device Usage", most_common_device)
col4.metric("🏃 Typical Physical Activity", most_common_exercise)

# --- Show Data ---
with st.expander("🔍 View Dataset"):
    st.dataframe(df.head())

# ==============================================
# 🎯 OBJECTIVE 2
# ==============================================
st.markdown("""
## 🎯 **Objective 2**
To analyze how students lifestyle behaviors — including **caffeine consumption**, **physical activity**, and **electronic device usage** — influence their overall **sleep quality** and **sleep duration**.
""")

# ==========================================================
# 1️⃣ Correlation Heatmap – Behaviors vs Sleep Issues
# ==========================================================
st.subheader("🧠 Correlation Between Lifestyle Behaviors and Sleep Issues")

behavior_sleep_df = df[[
    '3. How often do you have difficulty falling asleep at night? ',
    '5. How often do you wake up during the night and have trouble falling back asleep?',
    '6. How would you rate the overall quality of your sleep?',
    '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?',
    '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?',
    '13. How often do you engage in physical activity or exercise?'
]].copy()

behavior_sleep_df.columns = [
    'Difficulty falling asleep',
    'Nighttime awakenings',
    'Overall sleep quality',
    'Electronic device use',
    'Caffeine consumption',
    'Physical activity'
]

for col in behavior_sleep_df.columns:
    behavior_sleep_df[col], _ = pd.factorize(behavior_sleep_df[col])

correlation_matrix = behavior_sleep_df.corr()

fig1 = ff.create_annotated_heatmap(
    z=correlation_matrix.values,
    x=list(correlation_matrix.columns),
    y=list(correlation_matrix.index),
    annotation_text=correlation_matrix.round(2).values,
    colorscale=px.colors.sequential.Sunset,
    showscale=True
)
fig1.update_layout(
    title="Correlation Matrix: Lifestyle Behaviors vs Sleep Factors",
    xaxis_title="Variables",
    yaxis_title="Variables",
    title_font=dict(size=18)
)
st.plotly_chart(fig1, use_container_width=True)

# ==========================================================
# 2️⃣ Heatmap – Sleep Hours vs Device Use
# ==========================================================
st.subheader("📱 Relationship Between Sleep Hours and Device Use Before Bed")

sleep_device_df = df[['4. On average, how many hours of sleep do you get on a typical day?',
                      '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?']].copy()
sleep_device_df.columns = ['Average sleep hours', 'Device use before sleep']

sleep_hour_mapping = {'Less than 4 hours': 3, '4-5 hours': 4.5, '5-6 hours': 5.5,
                      '6-7 hours': 6.5, '7-8 hours': 7.5, 'More than 8 hours': 9}
device_use_mapping = {'Never': 0, 'Rarely (1-2 times a week)': 1.5, 'Sometimes (3-4 times a week)': 3.5,
                      'Often (5-6 times a week)': 5.5, 'Every night': 7}

sleep_device_df['Sleep_numeric'] = sleep_device_df['Average sleep hours'].map(sleep_hour_mapping)
sleep_device_df['Device_numeric'] = sleep_device_df['Device use before sleep'].map(device_use_mapping)

heatmap_data = sleep_device_df.pivot_table(
    index='Sleep_numeric',
    columns='Device_numeric',
    aggfunc='size',
    fill_value=0
)

fig2 = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=list(device_use_mapping.keys()),
    y=list(sleep_hour_mapping.keys()),
    colorscale='Sunset',
    colorbar=dict(title='Count')
))

fig2.update_layout(
    title='Density of Observations: Sleep Hours vs Device Use Before Sleep',
    xaxis_title='Device Use Frequency',
    yaxis_title='Average Sleep Hours',
)
st.plotly_chart(fig2, use_container_width=True)

# ==========================================================
# 3️⃣ Grouped Bar Chart – Sleep Quality by Caffeine Frequency
# ==========================================================
st.subheader("☕ Sleep Quality Across Different Caffeine Consumption Levels")

caffeine_sleep_df = df[df['12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?'].isin([
    'Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every day'
])].copy()

caffeine_sleep_crosstab = pd.crosstab(
    caffeine_sleep_df['12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?'],
    caffeine_sleep_df['6. How would you rate the overall quality of your sleep?'],
    normalize='index'
).reset_index().melt(
    id_vars='12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?',
    var_name='Sleep Quality',
    value_name='Proportion'
)

fig3 = px.bar(
    caffeine_sleep_crosstab,
    x='12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?',
    y='Proportion',
    color='Sleep Quality',
    barmode='group',
    title='Sleep Quality Ratings by Caffeine Frequency',
    labels={
        '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?': 'Caffeine Consumption Frequency',
        'Sleep Quality': 'Sleep Quality',
        'Proportion': 'Proportion of Students'
    },
    color_discrete_sequence=px.colors.sequential.Sunset
)

fig3.update_layout(legend_title_text="Sleep Quality")
st.plotly_chart(fig3, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("✅ *Developed with Streamlit + Plotly | Dataset: Student Insomnia and Educational Outcomes*")
