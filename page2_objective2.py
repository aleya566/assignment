import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# --- Streamlit Page Config ---
st.set_page_config(page_title="Student Lifestyle & Sleep Analysis", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Page Title ---
st.title("😴 Student Lifestyle Behaviors and Sleep Quality Dashboard")

st.markdown("""
Analyze how **caffeine consumption**, **physical activity**, and **device usage** influence students' **sleep quality**.
""")

# ==============================================
# 🔹 Key Metrics Section (matching Objective 1)
# ==============================================
col1, col2, col3, col4 = st.columns(4)

# Columns of interest
sleep_quality_col = '6. How would you rate the overall quality of your sleep?'
caffeine_col = '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?'
device_col = '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?'
exercise_col = '13. How often do you engage in physical activity or exercise?'

# Calculate key metrics
most_common_sleep_quality = df[sleep_quality_col].mode()[0] if not df[sleep_quality_col].empty else "N/A"
most_common_caffeine = df[caffeine_col].mode()[0] if not df[caffeine_col].empty else "N/A"
most_common_device = df[device_col].mode()[0] if not df[device_col].empty else "N/A"
most_common_exercise = df[exercise_col].mode()[0] if not df[exercise_col].empty else "N/A"

# --- Display Metrics with Plain Grey Borders ---

col1.metric(
    label="💤 Most Common Sleep Quality",
    value=most_common_sleep_quality,
    help="Most frequently reported sleep quality rating",
    border=True
)
col2.metric(
    label="☕ Typical Caffeine Use",
    value=most_common_caffeine,
    help="Most common caffeine consumption frequency",
    border=True
)
col3.metric(
    label="📱 Typical Device Usage",
    value=most_common_device,
    help="Most common frequency of device use before sleep",
    border=True
)
col4.metric(
    label="🏃 Typical Physical Activity",
    value=most_common_exercise,
    help="Most common frequency of physical activity",
    border=True
)

# --- Show Data ---
with st.expander("🔍 View Dataset"):
    st.dataframe(df.head())

# ==========================================================
# 1️⃣ Correlation Heatmap – Behaviors vs Sleep Issues
# ==========================================================
st.subheader("🧠 Correlation: Lifestyle Behaviors vs Sleep Issues")

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
    'Electronic device use before sleep',
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
    title="Correlation Matrix of Behaviors and Sleep Issues",
    xaxis=dict(title="Variables"),
    yaxis=dict(title="Variables"),
    title_font=dict(size=18)
)
st.plotly_chart(fig1, use_container_width=True)

# ==========================================================
# 2️⃣ Heatmap – Sleep Hours vs Device Use
# ==========================================================
st.subheader("📱 Average Sleep Hours vs Electronic Device Use Before Sleep")

sleep_device_df = df[[
    '4. On average, how many hours of sleep do you get on a typical day?',
    '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?'
]].copy()

sleep_device_df.columns = ['Average hours of sleep', 'Electronic device use before sleep']

sleep_hour_mapping = {
    'Less than 4 hours': 3, '4-5 hours': 4.5, '5-6 hours': 5.5,
    '6-7 hours': 6.5, '7-8 hours': 7.5, 'More than 8 hours': 9
}
device_use_mapping = {
    'Never': 0, 'Rarely (1-2 times a week)': 1.5, 'Sometimes (3-4 times a week)': 3.5,
    'Often (5-6 times a week)': 5.5, 'Every night': 7
}

sleep_device_df['Sleep_hours_numeric'] = sleep_device_df['Average hours of sleep'].map(sleep_hour_mapping)
sleep_device_df['Device_use_numeric'] = sleep_device_df['Electronic device use before sleep'].map(device_use_mapping)

heatmap_data = sleep_device_df.pivot_table(
    index='Sleep_hours_numeric',
    columns='Device_use_numeric',
    aggfunc='size',
    fill_value=0
)

fig2 = px.imshow(
    heatmap_data,
    text_auto=True,
    color_continuous_scale='Sunset',
    title='Density of Observations: Average Sleep Hours vs Device Use'
)
fig2.update_layout(
    xaxis_title="Device Use Frequency (Numeric Scale)",
    yaxis_title="Average Sleep Hours (Numeric Scale)"
)
st.plotly_chart(fig2, use_container_width=True)

# ==========================================================
# 3️⃣ Grouped Bar Chart – Sleep Quality by Caffeine Frequency
# ==========================================================
st.subheader("☕ Sleep Quality Ratings by Caffeine Consumption Frequency")

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
st.markdown("✅ *Developed with Streamlit + Plotly | Dataset: Student Insomnia and Educational Outcomes*")
