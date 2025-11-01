import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# --- Streamlit Page Config ---
st.set_page_config(page_title="Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance", layout="wide")

# --- Load Dataset ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)
    return df

df = load_data()


# --- Page Header ---
st.title("🧠 Interpretation Dashboard: Impact of Sleep Related Issues on Academic Performance")

# ==============================================
# 🔹 Key Metrics Section
# ==============================================
col1, col2, col3, col4 = st.columns(4)

# Define key columns
performance_col = '15. How would you rate your overall academic performance (GPA or grades) in the past semester?'
concentration_col = '7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?'
fatigue_col = '8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?'
sleep_impact_col = '10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?'

# Calculate summary metrics
common_performance = df[performance_col].mode()[0] if not df[performance_col].empty else "N/A"
common_concentration = df[concentration_col].mode()[0] if not df[concentration_col].empty else "N/A"
common_fatigue = df[fatigue_col].mode()[0] if not df[fatigue_col].empty else "N/A"
common_sleep_impact = df[sleep_impact_col].mode()[0] if not df[sleep_impact_col].empty else "N/A"

# Display metrics
# --- Display Metrics --- 
col1.metric(
label="🎓 Most Common Academic Performance",
value=common_performance, 
help="Most frequently reported academic performance level", 
border=True 
) 

col2.metric( 
label="🧩 Common Concentration Difficulty", 
value=common_concentration, 
help="Most common frequency of difficulty concentrating", 
border=True
) 

col3.metric( 
label="💤 Typical Fatigue Level", 
value=common_fatigue, 
help="Most common fatigue frequency reported by students", 
border=True
) 

col4.metric( 
label="📦 Impact of Insufficient Sleep", 
value=common_sleep_impact, 
help="Most common reported impact of insufficient sleep on assignments", 
border=True
)

# --- Dataset Preview ---
with st.expander("🔍 View Dataset"):
    st.dataframe(df.head())

# ==============================================
# 🎯 OBJECTIVE 3
# ==============================================
st.markdown("""
## 🎯 **Objective 3**
To investigate how sleep related issues such as **insufficient rest**, **difficulty concentrating** and **daytime fatigue** affect students **academic performance** and **cognitive functioning**. This objective focuses on understanding how **sleep deprivation and mental exhaustion** translate into measurable impacts on students’ learning efficiency, task completion, and overall academic results. 
""")

# =====================================================
# 1️⃣ Box Plot – Academic Performance vs Insufficient Sleep Impact
# =====================================================
st.subheader("a) Academic Performance by Impact of Insufficient Sleep on Assignments")
st.markdown("""
Students who reported a greater impact of insufficient sleep showed lower median academic performance. Those who said sleep deprivation had 'No Impact' achieved higher scores, while those who reported 'Severe Impact' tend to have the lowest grades. This visualization highlights the clear negative relationship between poor sleep and academic achievement.
""")

academic_performance_mapping = {'Poor': 1, 'Below Average': 2, 'Average': 3, 'Good': 4, 'Excellent': 5}
df['Academic Performance (Numeric)'] = df[performance_col].map(academic_performance_mapping)

impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']

fig1 = px.box(
    df,
    x=sleep_impact_col,
    y='Academic Performance (Numeric)',
    color=sleep_impact_col,
    category_orders={sleep_impact_col: impact_order},
    color_discrete_sequence=px.colors.sequential.Sunset,
    title="Academic Performance by Impact of Insufficient Sleep on Assignments"
)
fig1.update_layout(
    xaxis_title="Impact of Insufficient Sleep on Assignments",
    yaxis_title="Academic Performance (Numeric Scale)",
    legend_title_text="Sleep Impact Level",
    xaxis_tickangle=45
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# 2️⃣ Heatmap – Concentration Difficulty vs Fatigue vs Academic Performance
# =====================================================
st.subheader("b) Academic Performance by Fatigue and Concentration Difficulty")
st.markdown("""
Higher academic performance was concentrated among students who rarely feel fatigued or lost focus. As fatigue and concentration difficulty increase, grade point averages decreased. This pattern suggests that daytime fatigue and poor focus together contribute to lower academic outcomes.
""")
# Mapping categorical responses to numeric
mapping_scale = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4}
df['Concentration Difficulty (Numeric)'] = df[concentration_col].map(mapping_scale)
df['Fatigue Frequency (Numeric)'] = df[fatigue_col].map(mapping_scale)

# Pivot table
heatmap_data = df.pivot_table(
    index='Concentration Difficulty (Numeric)',
    columns='Fatigue Frequency (Numeric)',
    values='Academic Performance (Numeric)',
    aggfunc='mean'
)

fig2 = px.imshow(
    heatmap_data,
    text_auto=True,
    color_continuous_scale='Sunset',
    title="Academic Performance by Fatigue and Concentration Difficulty",
    labels=dict(x="Fatigue Frequency", y="Concentration Difficulty", color="Avg Academic Perf.")
)
fig2.update_layout(
    xaxis_title="Fatigue Frequency (Numeric Scale)",
    yaxis_title="Concentration Difficulty (Numeric Scale)",
    coloraxis_colorbar=dict(title="Performance"),
    height=600,  # ✅ same height
    margin=dict(l=80, r=20, t=70, b=100)  # ✅ same margins
)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3️⃣ Violin Plot – Academic Performance by Difficulty Concentrating
# =====================================================
st.subheader("c) Academic Performance by Difficulty Concentrating")
st.markdown("""
Students who never or rarely had struggle to concentrate tend to achieve better grades, with most results falling in the 'Good' to 'Excellent' range. As concentration difficulties increased to 'Often' and 'Always', performance shifted downward, clustering around 'Average' or 'Below Average'. This reinforces that cognitive impairment due to poor sleep directly reduces academic success.
""")

fig3 = px.violin(
    df,
    x=concentration_col,
    y='Academic Performance (Numeric)',
    color=concentration_col,
    box=True,
    points='all',
    category_orders={concentration_col: ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']},
    color_discrete_sequence=px.colors.sequential.Sunset,
    title="Academic Performance by Difficulty Concentrating"
)
fig3.update_layout(
    xaxis_title="Difficulty Concentrating Frequency",
    yaxis_title="Academic Performance (Numeric Scale)",
    legend_title_text="Concentration Level",
    xaxis_tickangle=45,
    height=600,  # same as the box plot shown in your screenshot
    margin=dict(l=60, r=40, t=70, b=80),
    title_font=dict(size=18)
)
st.plotly_chart(fig3, use_container_width=True)

# --- Footer ---
st.markdown("---")
