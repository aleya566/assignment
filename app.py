import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads and caches the dataset."""
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# Rename long columns for easier use in charts
df.rename(columns={
    '1. What is your year of study?': 'Year_of_Study',
    '2. What is your gender?': 'Gender',
    '4. On average, how many hours of sleep do you get on a typical day?': 'Avg_Sleep_Hours',
    '6. How would you rate the overall quality of your sleep?': 'Sleep_Quality',
    '14. How would you describe your stress levels related to academic workload?': 'Academic_Stress_Level',
    '15. How would you rate your overall academic performance (GPA or grades) in the past semester?': 'Academic_Performance'
}, inplace=True)

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Student Sleep and Academic Factors Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('📚 Student Sleep and Academic Factors Dashboard')
st.markdown("""
This dashboard explores the relationship between sleep, stress, and academic factors among students using interactive **Plotly** charts.
""")

st.sidebar.header('Dataset Information')
if st.sidebar.checkbox('Show Raw Data'):
    st.subheader('Raw Dataset Head')
    st.dataframe(df.head())
    st.caption(f"Total Rows: {len(df)}")
    
st.sidebar.markdown('---')
st.sidebar.header('Chart Customization')

# --- Plotly Visualization Functions ---

def create_stress_by_year_plot(data):
    """Creates an interactive Stacked Bar Chart for Stress Levels by Year of Study."""
    st.subheader('📈 Academic Stress Levels by Year of Study')
    st.markdown("Examines the **proportion** of students reporting different stress levels across years of study.")
    
    # Calculate the proportion (crosstab and normalize)
    stress_year_crosstab = pd.crosstab(data['Year_of_Study'], data['Academic_Stress_Level'], normalize='index').stack().reset_index(name='Proportion')
    stress_year_crosstab.columns = ['Year_of_Study', 'Academic_Stress_Level', 'Proportion']
    
    # Define a custom order for the stress levels
    stress_order = ['Low', 'Moderate', 'High', 'Very High']
    stress_year_crosstab['Academic_Stress_Level'] = pd.Categorical(stress_year_crosstab['Academic_Stress_Level'], categories=stress_order, ordered=True)
    stress_year_crosstab.sort_values(by='Academic_Stress_Level', inplace=True)
    
    # Create the Plotly figure
    fig = px.bar(
        stress_year_crosstab,
        x='Year_of_Study',
        y='Proportion',
        color='Academic_Stress_Level',
        title='Academic Stress Levels by Year of Study (Proportion)',
        labels={'Year_of_Study': 'Year of Study', 'Proportion': 'Proportion of Students', 'Academic_Stress_Level': 'Stress Level'},
        color_discrete_sequence=px.colors.sequential.Sunset, # Use a color sequence similar to 'flare'
        category_orders={"Academic_Stress_Level": stress_order}
    )
    
    # Customizing the layout to ensure stacking
    fig.update_layout(
        barmode='stack', 
        yaxis_tickformat='.0%', # Format y-axis as percentage
        xaxis={'categoryorder': 'array', 'categoryarray': sorted(data['Year_of_Study'].unique())}
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_sleep_hours_by_gender_plot(data):
    """Creates an interactive Box Plot for Average Sleep Hours by Gender."""
    st.subheader('🛌 Average Sleep Hours by Gender')
    st.markdown("Visualizes the **distribution** of average sleep hours for male and female students.")

    # Get user selected colors from the sidebar
    selected_palette = st.sidebar.selectbox(
        'Select Color Palette for Sleep Hours Plot:',
        ['Plotly', 'Dark2', 'Set1', 'Sunset']
    )
    
    if selected_palette == 'Plotly':
        colors = px.colors.qualitative.Plotly
    elif selected_palette == 'Dark2':
        colors = px.colors.qualitative.Dark2
    elif selected_palette == 'Set1':
        colors = px.colors.qualitative.Set1
    else:
        colors = px.colors.sequential.Sunset
        
    # Create the Plotly figure
    fig = px.box(
        data,
        x='Gender',
        y='Avg_Sleep_Hours',
        color='Gender',
        category_orders={"Gender": ['Male', 'Female']},
        title='Average Sleep Hours by Gender (Box Plot)',
        labels={'Gender': 'Gender', 'Avg_Sleep_Hours': 'Average Sleep Hours'},
        color_discrete_sequence=colors,
        notched=st.sidebar.checkbox('Notched Box Plot?', value=False)
    )
    
    fig.update_traces(quartilemethod="exclusive") # Standard quartile method
    
    st.plotly_chart(fig, use_container_width=True)

def create_sleep_quality_vs_performance_plot(data):
    """Creates an interactive Stacked Bar Chart for Sleep Quality vs Academic Performance."""
    st.subheader('⭐ Sleep Quality vs Academic Performance')
    st.markdown("Shows the **proportion** of students in each sleep quality category reporting different levels of academic performance.")
    
    # Calculate the proportion (crosstab and normalize)
    cross_tab = pd.crosstab(data['Sleep_Quality'], data['Academic_Performance'], normalize='index').stack().reset_index(name='Proportion')
    cross_tab.columns = ['Sleep_Quality', 'Academic_Performance', 'Proportion']
    
    # Define custom orders for visualization
    quality_order = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
    performance_order = ['Below Average', 'Average', 'Good', 'Excellent']

    cross_tab['Sleep_Quality'] = pd.Categorical(cross_tab['Sleep_Quality'], categories=quality_order, ordered=True)
    cross_tab['Academic_Performance'] = pd.Categorical(cross_tab['Academic_Performance'], categories=performance_order, ordered=True)
    cross_tab.sort_values(by=['Sleep_Quality', 'Academic_Performance'], inplace=True)
    
    # Create the Plotly figure
    fig = px.bar(
        cross_tab,
        x='Sleep_Quality',
        y='Proportion',
        color='Academic_Performance',
        title='Sleep Quality vs Academic Performance (Proportion)',
        labels={'Sleep_Quality': 'Overall Sleep Quality', 'Proportion': 'Proportion', 'Academic_Performance': 'Academic Performance'},
        color_discrete_sequence=px.colors.sequential.Viridis,
        category_orders={"Sleep_Quality": quality_order, "Academic_Performance": performance_order}
    )
    
    fig.update_layout(
        barmode='stack', 
        yaxis_tickformat='.0%',
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- Main App Layout ---
# Use columns for a cleaner, side-by-side layout
col1, col2 = st.columns(2)

with col1:
    create_stress_by_year_plot(df)

with col2:
    create_sleep_hours_by_gender_plot(df)

st.markdown('---')

create_sleep_quality_vs_performance_plot(df)
