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


# --- Define logical order for all categorical columns ---

category_orders = {
    # Year of study
    '1. What is your year of study?': [
        'First year', 'Second year', 'Third year', 'Graduate student'
    ],

    # Gender
    '2. What is your gender?': [
        'Male', 'Female'
    ],

    # Sleep difficulty frequency
    '3. How often do you have difficulty falling asleep at night? ': [
        'Never',
        'Rarely (1-2 times a week)',
        'Sometimes (3-4 times a week)',
        'Often (5-6 times a week)',
        'Every night'
    ],

    # Average sleep hours
    '4. On average, how many hours of sleep do you get on a typical day?': [
        'Less than 4 hours',
        '4-5 hours',
        '6-7 hours',
        '7-8 hours',
        'More than 8 hours'
    ],

    # Waking up and trouble falling asleep
    '5. How often do you wake up during the night and have trouble falling back asleep?': [
        'Never',
        'Rarely (1-2 times a week)',
        'Sometimes (3-4 times a week)',
        'Often (5-6 times a week)',
        'Every night'
    ],

    # Overall sleep quality
    '6. How would you rate the overall quality of your sleep?': [
        'Very poor',
        'Poor',
        'Average',
        'Good',
        'Very good'
    ],

    # Difficulty concentrating
    '7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?': [
        'Never', 'Rarely', 'Sometimes', 'Often', 'Always'
    ],

    # Fatigue during the day
    '8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?': [
        'Never', 'Rarely', 'Sometimes', 'Often', 'Always'
    ],

    # Missing/skipping classes
    '9. How often do you miss or skip classes due to sleep-related issues (e.g., insomnia, feeling tired)?': [
        'Never',
        'Rarely (1-2 times a month)',
        'Sometimes (1-2 times a week)',
        'Often (3-4 times a week)',
        'Always'
    ],

    # Impact of insufficient sleep
    '10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?': [
        'No impact',
        'Minor impact',
        'Moderate impact',
        'Major impact',
        'Severe impact'
    ],

    # Use of electronic devices
    '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?': [
        'Never',
        'Rarely (1-2 times a week)',
        'Sometimes (3-4 times a week)',
        'Often (5-6 times a week)',
        'Every night'
    ],

    # Caffeine consumption
    '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?': [
        'Never',
        'Rarely (1-2 times a week)',
        'Sometimes (3-4 times a week)',
        'Often (5-6 times a week)',
        'Every day'
    ],

    # Physical activity
    '13. How often do you engage in physical activity or exercise?': [
        'Never',
        'Rarely (1-2 times a week)',
        'Sometimes (3-4 times a week)',
        'Often (5-6 times a week)',
        'Every day'
    ],

    # Academic stress levels
    '14. How would you describe your stress levels related to academic workload?': [
        'No stress', 'Low stress', 'High stress', 'Extremely high stress'
    ],

    # Academic performance
    '15. How would you rate your overall academic performance (GPA or grades) in the past semester?': [
        'Poor', 'Below Average', 'Average', 'Good', 'Excellent'
    ]
}

# --- Apply all orders automatically ---
for col, order in category_orders.items():
    if col in df.columns:
        df[col] = pd.Categorical(df[col], categories=order, ordered=True)



# --- Page Title ---
st.title("🔎 Exploration Dashboard: Academic Stress and Sleep Patterns Among Students")

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
st.subheader("a) Academic Stress Levels by Year of Study")

st.markdown("""
This visualization shows that graduate students experience the highest proportion of 'Extremely High Stress' and followed by third year students. First year and Second year students seem to have a slightly lower proportion of the highest stress levels compared to third year and graduate students. This trend suggests that academic workload and expectations increase as students advance through their studies which reaching a peak at the graduate level.
""")

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
st.subheader("b) Average Sleep Hours by Gender")

st.markdown("""
This box plot shows both male and female students report a similar median of 7–8 hours of sleep, with comparable interquartile ranges. 
A few outliers show students sleeping far less or more than typical. Overall, gender does not appear to significantly affect average 
sleep duration among students in this dataset.
""")

# Define column names
gender_col = '2. What is your gender?'
sleep_col = '4. On average, how many hours of sleep do you get on a typical day?'

# Set gender order explicitly
gender_order = ['Male', 'Female']

# Create box plot
fig2 = px.box(
    df,
    x=gender_col,
    y=sleep_col,
    color=gender_col,
    category_orders={gender_col: gender_order},  # ✅ ensures same order as Seaborn
    title='Average Sleep Hours by Gender',
    labels={
        gender_col: 'Gender',
        sleep_col: 'Average Sleep Hours'
    },
    color_discrete_sequence=px.colors.sequential.Sunset,  # similar to 'flare'
    points="all"  # ✅ show all outliers like Seaborn
)

# Update layout for consistent look
fig2.update_layout(
    xaxis_title="Gender",
    yaxis_title="Average Sleep Hours",
    showlegend=False,
    boxmode='group'
)

# Display in Streamlit
st.plotly_chart(fig2, use_container_width=True)




# ==============================================
# 3️⃣ Stacked Bar Chart – Sleep Quality by Year of Study
# ==============================================
st.subheader("c) Sleep Quality by Year of Study")
st.markdown("""
Most students, regardless of year, reported 'Poor' or 'Very Poor' sleep quality. However, graduate and third year students showed a higher percentage of 'Very Poor' sleep, while first and second year students reported slightly higher 'Good' sleep quality. This pattern suggests that sleep quality challenges persist across all levels, possibly worsening due to academic stress.
""")

# 🧹 STEP 1: Clean and standardize text (important for correct category matching)
df['1. What is your year of study?'] = (
    df['1. What is your year of study?']
    .str.strip()
    .str.title()  # e.g., 'Graduate Student'
)

df['6. How would you rate the overall quality of your sleep?'] = (
    df['6. How would you rate the overall quality of your sleep?']
    .str.strip()
    .str.title()  # e.g., 'Very Poor', 'Good', etc.
)

# 🧭 STEP 2: Define correct logical orders
year_of_study_order = ['First Year', 'Second Year', 'Third Year', 'Graduate Student']
sleep_quality_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good']

# 🗂️ STEP 3: Convert to categorical type with specified order
df['1. What is your year of study?'] = pd.Categorical(
    df['1. What is your year of study?'],
    categories=year_of_study_order,
    ordered=True
)

df['6. How would you rate the overall quality of your sleep?'] = pd.Categorical(
    df['6. How would you rate the overall quality of your sleep?'],
    categories=sleep_quality_order,
    ordered=True
)

# 📊 STEP 4: Create crosstab for proportions
sleep_quality_year_crosstab = pd.crosstab(
    df['1. What is your year of study?'],
    df['6. How would you rate the overall quality of your sleep?'],
    normalize='index'
)

# 📈 STEP 5: Reshape data for Plotly
plot_data_sleep_year = sleep_quality_year_crosstab.reset_index().melt(
    id_vars='1. What is your year of study?',
    var_name='Sleep Quality',
    value_name='Proportion'
)

# 🎨 STEP 6: Plot stacked bar chart
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
    labels={
        '1. What is your year of study?': 'Year of Study',
        'Proportion': 'Proportion of Students'
    },
    color_discrete_sequence=px.colors.sequential.Sunset
)

fig_sleep_year.update_layout(legend_title_text="Sleep Quality")

# 📤 STEP 7: Display in Streamlit
st.plotly_chart(fig_sleep_year, use_container_width=True)

# --- Footer ---
st.markdown("---")
