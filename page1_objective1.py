import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np  # Included for robust category ordering

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
st.title("🔎 Exploration Dashboard: Academic Stress and Sleep Patterns Among Students")

st.markdown("""
Explore the relationships between **sleep habits, stress levels, and academic performance** among students.
""")

# ==============================================
# 🔹 Key Metrics Section
# ==============================================
col1, col2, col3, col4 = st.columns(4)

# Clean numeric values for sleep hours
sleep_col = '4. On average, how many hours of sleep do you get on a typical day?'

df[sleep_col] = df[sleep_col].astype(str).str.extract(r'(\d+\.?\d*)')
df[sleep_col] = pd.to_numeric(df[sleep_col], errors='coerce')

# Compute summary metrics
avg_sleep = df[sleep_col].mean()

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
# 🎯 OBJECTIVE 1
# ==============================================
st.markdown("""
## 🎯 **Objective 1**
To explore how academic stress levels and sleep patterns vary across students years of study and genders. This objective focuses on identifying patterns of **academic stress**, **sleep duration** and **sleep quality** across different groups of students.
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
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Define the categories and their desired order for consistent plotting
GENDER_ORDER = ['Male', 'Female']
SLEEP_HOURS_ORDER = ['Less than 4 hours', '4-5 hours', '5-6 hours', 
                     '6-7 hours', '7-8 hours', 'More than 8 hours']

def app():
    st.title("😴 Box Plot: Average Sleep Hours by Gender")
    st.write("Visualizing the distribution of average sleep hours for male and female students.")

    # =================================================================
    # NOTE: You MUST replace this dummy data creation block with your 
    # actual code to load your DataFrame (e.g., df = pd.read_csv('your_data.csv')).
    # The columns must be named '2. What is your gender?' and 
    # '4. On average, how many hours of sleep do you get on a typical day?'.
    # =================================================================
    

    # --- Plotly Box Plot Visualization ---
    
    fig = px.box(
        df,
        x='2. What is your gender?',
        y='4. On average, how many hours of sleep do you get on a typical day?',
        color='2. What is your gender?', # Used for color differentiation (like Seaborn's hue)
        color_discrete_sequence=px.colors.sequential.Plasma, # A color scheme similar to 'flare'
        category_orders={
            # Enforce the order for the x-axis (Gender)
            '2. What is your gender?': GENDER_ORDER, 
            # Enforce the order for the y-axis (Sleep Hours)
            '4. On average, how many hours of sleep do you get on a typical day?': SLEEP_HOURS_ORDER
        },
        orientation='v', # Vertical box plots
        title='Average Sleep Hours by Gender'
    )
    
    # Update layout for cleaner presentation, matching the original request
    fig.update_layout(
        xaxis_title='Gender',
        yaxis_title='Average Sleep Hours',
        # Remove the legend since the color is the same as the x-axis
        showlegend=False,
        # Ensure the y-axis categories are displayed correctly
        yaxis={'categoryorder': 'array', 'categoryarray': SLEEP_HOURS_ORDER},
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    # Streamlit entry point: run this script using `streamlit run <filename>.py`
    app()

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
    color_discrete_sequence=px.colors.sequential.Sunset

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
