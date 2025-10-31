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
st.title("🎓 Analysis Dashboard: Lifestyle Behaviors and Their Influence on Sleep Quality")

st.markdown("""
Analyze how **caffeine consumption**, **physical activity**, and **device usage** influence students' **sleep quality**.
""")

# ==============================================
# 🔹 Key Metrics Section
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

# ==============================================
# 🎯 OBJECTIVE 2
# ==============================================
st.markdown("""
## 🎯 **Objective 2**
To analyze how students lifestyle behaviors — including **caffeine consumption**, **physical activity** and **electronic device usage** — influence their overall **sleep quality** and **sleep duration**. This objective focuses on identifying the behavioral factors that may contribute to **sleep disturbances** and **variations in sleep quality** among students.
""")

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
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Streamlit Application Code ---
def app():
    # Set the title and a brief description
    st.title("😴 Sleep Hours vs. Electronic Device Use Heatmap")
    st.write("Density of Observations for Different Combinations of Average Sleep Hours and Electronic Device Use Before Sleep (Plotly Heatmap)")
    
    # =================================================================
    # NOTE: You MUST replace this dummy data with your actual DataFrame
    # loaded from your source (e.g., df = pd.read_csv('your_data.csv'))
    # The columns '4...' and '11...' must match your original data.
    # =================================================================
    

    # --- Data Processing (as provided in your original script) ---

    # Select relevant columns
    sleep_device_df = df[['4. On average, how many hours of sleep do you get on a typical day?',
                          '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?']].copy()

    # Rename columns for clarity
    sleep_device_df.columns = ['Average hours of sleep', 'Electronic device use before sleep']

    # Map categorical sleep hours to numerical values
    sleep_hour_mapping = {'Less than 4 hours': 3, '4-5 hours': 4.5, '5-6 hours': 5.5,
                          '6-7 hours': 6.5, '7-8 hours': 7.5, 'More than 8 hours': 9}

    sleep_device_df['Average hours of sleep_numeric'] = sleep_device_df['Average hours of sleep'].map(sleep_hour_mapping)

    # Map categorical device use to numerical values
    device_use_mapping = {'Never': 0, 'Rarely (1-2 times a week)': 1.5, 'Sometimes (3-4 times a week)': 3.5,
                          'Often (5-6 times a week)': 5.5, 'Every night': 7}

    sleep_device_df['Electronic device use before sleep_numeric'] = sleep_device_df['Electronic device use before sleep'].map(device_use_mapping)

    # Create a pivot table to count occurrences
    heatmap_data = sleep_device_df.pivot_table(index='Average hours of sleep_numeric',
                                               columns='Electronic device use before sleep_numeric',
                                               aggfunc='size', fill_value=0)

    # Reorder index and columns for logical display using the numeric keys
    sleep_keys_ordered = list(sleep_hour_mapping.values())
    device_keys_ordered = list(device_use_mapping.values())
    
    # Reindex to ensure order and fill any missing combinations with 0
    heatmap_data = heatmap_data.reindex(sleep_keys_ordered)
    heatmap_data = heatmap_data.T.reindex(device_keys_ordered).T.fillna(0)
    
    # Get the ordered categorical labels for plotting
    sleep_hour_labels = list(sleep_hour_mapping.keys())
    device_use_labels = list(device_use_mapping.keys())
    
    # --- Plotly Visualization (Conversion from Matplotlib/Seaborn) ---
    
    # Get the Z data (counts)
    z_data = heatmap_data.values.tolist()

    # Create the Heatmap trace
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=device_use_labels,
        y=sleep_hour_labels,
        colorscale='Sunset',  # Use a nice Plotly colorscale
        colorbar=dict(title='Count'),
        text=np.array(z_data).astype(str), # Text for annotation
        texttemplate="%{text}", # Display the text
        textfont={"size": 12, "color": "black"}
    ))

    # Update layout for titles and axis formatting
    fig.update_layout(
        title='Density of Observations: Average Hours of Sleep vs. Electronic Device Use Before Sleep',
        xaxis_title='Frequency of Electronic Device Use Before Sleep',
        yaxis_title='Average Hours of Sleep',
        # Reverse Y-axis to match typical heatmap layout (lower indices at top)
        yaxis=dict(autorange='reversed'), 
        height=600,
        margin=dict(l=80, r=20, t=70, b=100)
    )

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    # Streamlit entry point: run this script using `streamlit run <script_name>.py`
    app()

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
