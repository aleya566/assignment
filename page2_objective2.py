import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objects as go

# --- Streamlit Page Config ---
st.set_page_config(page_title="Analysis Dashboard: Lifestyle Behaviors and Their Influence on Sleep Quality", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Define logical order for all categorical columns ---
category_orders = {
    '1. What is your year of study?': ['First year', 'Second year', 'Third year', 'Graduate student'],
    '2. What is your gender?': ['Male', 'Female'],
    '3. How often do you have difficulty falling asleep at night? ': [
        'Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every night'],
    '4. On average, how many hours of sleep do you get on a typical day?': [
        'Less than 4 hours', '4-5 hours', '6-7 hours', '7-8 hours', 'More than 8 hours'],
    '5. How often do you wake up during the night and have trouble falling back asleep?': [
        'Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every night'],
    '6. How would you rate the overall quality of your sleep?': [
        'Very poor', 'Poor', 'Average', 'Good', 'Very good'],
    '7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?': [
        'Never', 'Rarely', 'Sometimes', 'Often', 'Always'],
    '8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?': [
        'Never', 'Rarely', 'Sometimes', 'Often', 'Always'],
    '9. How often do you miss or skip classes due to sleep-related issues (e.g., insomnia, feeling tired)?': [
        'Never', 'Rarely (1-2 times a month)', 'Sometimes (1-2 times a week)', 'Often (3-4 times a week)', 'Always'],
    '10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?': [
        'No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact'],
    '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?': [
        'Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every night'],
    '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?': [
        'Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every day'],
    '13. How often do you engage in physical activity or exercise?': [
        'Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every day'],
    '14. How would you describe your stress levels related to academic workload?': [
        'No stress', 'Low stress', 'High stress', 'Extremely high stress'],
    '15. How would you rate your overall academic performance (GPA or grades) in the past semester?': [
        'Poor', 'Below Average', 'Average', 'Good', 'Excellent']
}

# --- Apply all orders automatically ---
for col, order in category_orders.items():
    if col in df.columns:
        df[col] = pd.Categorical(df[col], categories=order, ordered=True)

# --- Page Title ---
st.title("📊 Analysis Dashboard: Lifestyle Behaviors and Their Influence on Sleep Quality")

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

col1.metric("💤 Most Common Sleep Quality", most_common_sleep_quality, help="Most frequently reported sleep quality rating")
col2.metric("☕ Typical Caffeine Use", most_common_caffeine, help="Most common caffeine consumption frequency")
col3.metric("📱 Typical Device Usage", most_common_device, help="Most common frequency of device use before sleep")
col4.metric("🏃 Typical Physical Activity", most_common_exercise, help="Most common frequency of physical activity")

# --- Show Data ---
with st.expander("🔍 View Dataset"):
    st.dataframe(df.head())

# ==============================================
# 🎯 OBJECTIVE 2
# ==============================================
st.markdown("""
## 🎯 **Objective 2**
To analyze how students lifestyle behaviors (including **caffeine consumption**, **physical activity** and **electronic device usage**) influence their overall **sleep quality** and **sleep duration**.
""")

# ==========================================================
# 1️⃣ Correlation Heatmap – Behaviors vs Sleep Issues
# ==========================================================
st.subheader("a) Correlation Between Lifestyle Behaviors and Sleep Issues")
st.markdown("""
A moderate positive correlation appears between electronic device use, caffeine intake and difficulty falling asleep. 
Nighttime awakenings also strongly correlate with frequent device use. 
Overall sleep quality shows a weak negative association, suggesting that increased screen time and caffeine may slightly worsen sleep patterns.
""")

behavior_sleep_df = df[[
    '3. How often do you have difficulty falling asleep at night? ',
    '5. How often do you wake up during the night and have trouble falling back asleep?',
    '6. How would you rate the overall quality of your sleep?',
    '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?',
    '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?',
    '13. How often do you engage in physical activity or exercise?'
]].copy()

behavior_sleep_df.columns = [
    'Difficulty falling asleep', 'Nighttime awakenings', 'Overall sleep quality',
    'Electronic device use before sleep', 'Caffeine consumption', 'Physical activity'
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
    showscale=True,
    colorbar=dict(title='Correlation')
)

fig1.update_layout(
    title="Correlation Between Lifestyle Behaviors and Sleep Issues",
    xaxis=dict(title="Variables"),
    yaxis=dict(title="Variables"),
    title_font=dict(size=18),
    height=600,  # ✅ same height
    margin=dict(l=80, r=20, t=70, b=100)  # ✅ same margins
)

st.plotly_chart(fig1, use_container_width=True)

# ==========================================================
# 2️⃣ Heatmap – Sleep Hours vs Device Use
# ==========================================================
st.subheader("b) Average Hours of Sleep vs. Electronic Device Use Before Sleep")
st.markdown("""
Most students slept 7–8 hours or more, even while using devices often or every night before bed.
This indicates that while device use before bed is common, it does not significantly reduce sleep duration,
although the quality of sleep may still be affected.
""")

sleep_device_df = df[['4. On average, how many hours of sleep do you get on a typical day?',
                      '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?']].copy()

sleep_device_df.columns = ['Average hours of sleep', 'Electronic device use before sleep']

sleep_hour_mapping = {'Less than 4 hours': 3, '4-5 hours': 4.5, '5-6 hours': 5.5,
                      '6-7 hours': 6.5, '7-8 hours': 7.5, 'More than 8 hours': 9}
device_use_mapping = {'Never': 0, 'Rarely (1-2 times a week)': 1.5, 'Sometimes (3-4 times a week)': 3.5,
                      'Often (5-6 times a week)': 5.5, 'Every night': 7}

sleep_device_df['Average hours of sleep_numeric'] = sleep_device_df['Average hours of sleep'].map(sleep_hour_mapping)
sleep_device_df['Electronic device use before sleep_numeric'] = sleep_device_df['Electronic device use before sleep'].map(device_use_mapping)

heatmap_data = sleep_device_df.pivot_table(
    index='Average hours of sleep_numeric',
    columns='Electronic device use before sleep_numeric',
    aggfunc='size', fill_value=0
)

heatmap_data = heatmap_data.reindex(list(sleep_hour_mapping.values()))
heatmap_data = heatmap_data.T.reindex(list(device_use_mapping.values())).T.fillna(0)

z_data = heatmap_data.values.tolist()

fig2 = go.Figure(data=go.Heatmap(
    z=z_data,
    x=list(device_use_mapping.keys()),
    y=list(sleep_hour_mapping.keys()),
    colorscale='Sunset',
    colorbar=dict(title='Count'),
    text=np.array(z_data).astype(str),
    texttemplate="%{text}",
    textfont={"size": 12, "color": "black"}
))

fig2.update_layout(
    title='Average Hours of Sleep vs. Electronic Device Use Before Sleep',
    xaxis_title='Frequency of Electronic Device Use Before Sleep',
    yaxis_title='Average Hours of Sleep',
    yaxis=dict(autorange='reversed'),
    height=600,  # ✅ same height
    margin=dict(l=80, r=20, t=70, b=100)  # ✅ same margins
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================================================
# 3️⃣ Grouped Bar Chart – Sleep Quality by Caffeine Frequency
# ==========================================================
st.subheader("c) Sleep Quality Ratings by Caffeine Consumption Frequency")
st.markdown("""
Students who never consume caffeine reported more 'Good' and 'Very Good' sleep quality.
As caffeine frequency increased, the proportion of 'Poor' and 'Very Poor' sleep rates also increased,
showing a negative trend between caffeine intake and sleep quality.
""")

caffeine_sleep_df = df[df['12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?)'].notna()].copy()
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
    title='Sleep Quality Ratings by Caffeine Consumption Frequency',
    color_discrete_sequence=px.colors.sequential.Sunset
)

fig3.update_layout(
    xaxis_title='Caffeine Consumption Frequency',
    yaxis_title='Proportion',
    xaxis_tickangle=45
)

st.plotly_chart(fig3, use_container_width=True)

# --- Footer ---
st.markdown("---")
