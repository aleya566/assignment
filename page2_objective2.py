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
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Data Mappings ---
sleep_hour_mapping = {'Less than 4 hours': 3, '4-5 hours': 4.5, '5-6 hours': 5.5,
                      '6-7 hours': 6.5, '7-8 hours': 7.5, 'More than 8 hours': 9}
device_use_mapping = {'Never': 0, 'Rarely (1-2 times a week)': 1.5, 'Sometimes (3-4 times a week)': 3.5,
                      'Often (5-6 times a week)': 5.5, 'Every night': 7}

# Assuming 'sleep_device_df' has been prepared as in your original script
# and 'heatmap_data' is the resulting pivot table (DataFrame with numeric indices/columns)

# --- Plotly Conversion ---

# Reorder heatmap_data to ensure categorical order
Y_numeric_order = list(sleep_hour_mapping.values())
X_numeric_order = list(device_use_mapping.values())

# Reindex using the numeric keys, fill NaNs (if any missing combinations)
heatmap_data = heatmap_data.reindex(index=Y_numeric_order,
                                    columns=X_numeric_order).fillna(0)

# Extract Z (counts), Y (Sleep Hours labels), and X (Device Use labels)
Z = heatmap_data.values.tolist()
Y = list(sleep_hour_mapping.keys())
X = list(device_use_mapping.keys())

# Create the heatmap trace
heatmap_trace = go.Heatmap(
    z=Z,
    x=X, # Categorical labels for x-axis
    y=Y, # Categorical labels for y-axis
    colorscale='Plasma',  # A perceptually uniform colorscale (similar to 'flare')
    hovertemplate='Sleep Hours: %{y}<br>Device Use: %{x}<br>Count: %{z}<extra></extra>',
    showscale=True
)

# Create the layout
layout = go.Layout(
    title='Density of Observations: Average Hours of Sleep vs. Electronic Device Use Before Sleep',
    xaxis=dict(
        title='Frequency of Electronic Device Use Before Sleep',
        tickangle=-45,
        automargin=True
    ),
    yaxis=dict(
        title='Average Hours of Sleep',
        automargin=True
    )
)

# Create the figure
fig = go.Figure(data=[heatmap_trace], layout=layout)

# Add annotations (text labels for the cell values, equivalent to annot=True in seaborn)
annotations = []
for i, y_label in enumerate(Y):
    for j, x_label in enumerate(X):
        count = Z[i][j]
        # Conditional text color for better contrast
        text_color = 'white' if count > np.median(Z) else 'black'
        annotations.append(go.layout.Annotation(
            x=x_label,
            y=y_label,
            text=str(int(count)), # Ensure integer format
            xref='x1',
            yref='y1',
            showarrow=False,
            font=dict(color=text_color)
        ))

fig.update_layout(annotations=annotations)

# fig.show() # Uncomment to display in a local environment
# fig.write_json("sleep_device_heatmap.json") # Save for Streamlit

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
