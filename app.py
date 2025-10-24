import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Configuration and Setup ---

# Set wide layout and title
st.set_page_config(
    layout="wide",
    page_title="Student Insomnia & Educational Outcomes Report",
    initial_sidebar_state="expanded"
)

# --- Data Loading and Preprocessing ---

@st.cache_data
def load_and_preprocess_data():
    """Loads the dataset from GitHub and performs necessary column renaming and mapping."""
    url = 'https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv'
    df = pd.read_csv(url)

    # Dictionary to rename the long question-based columns to short, usable names
    # Mapping based on the columns used in the user's Colab code
    column_rename_map = {
        '1. What is your year of study?': 'Year_of_Study',
        '2. What is your gender?': 'Gender',
        '3. How often do you have difficulty falling asleep at night? ': 'Difficulty_Falling_Asleep',
        '4. On average, how many hours of sleep do you get on a typical day?': 'Sleep_Hours',
        '5. How often do you wake up during the night and have trouble falling back asleep?': 'Nighttime_Awakenings',
        '6. How would you rate the overall quality of your sleep?': 'Sleep_Quality',
        '7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?': 'Difficulty_Concentrating',
        '8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?': 'Fatigue_Frequency',
        '10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?': 'Assignment_Impact',
        '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?': 'Device_Use_Before_Sleep',
        '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?': 'Caffeine_Consumption',
        '13. How often do you engage in physical activity or exercise?': 'Physical_Activity',
        '14. How would you describe your stress levels related to academic workload?': 'Academic_Stress',
        '15. How would you rate your overall academic performance (GPA or grades) in the past semester?': 'Academic_Performance_Rating'
    }
    
    df.rename(columns=column_rename_map, inplace=True)

    # --- Pre-calculate Numeric Mappings for Plotting ---
    
    # 1. Numeric GPA/Grades for Objective 3 Box/Heatmap
    academic_performance_mapping = {'Poor': 1, 'Below Average': 2, 'Average': 3, 'Good': 4, 'Excellent': 5}
    df['Academic_Performance_Numeric'] = df['Academic_Performance_Rating'].map(academic_performance_mapping)

    # 2. Numeric Concentration for Objective 3 Heatmap
    concentration_mapping = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4}
    df['Concentration_Numeric'] = df['Difficulty_Concentrating'].map(concentration_mapping)

    # 3. Numeric Fatigue for Objective 3 Heatmap
    fatigue_mapping = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4}
    df['Fatigue_Numeric'] = df['Fatigue_Frequency'].map(fatigue_mapping)

    return df

# Load the processed data
df = load_and_preprocess_data()


# Helper function for custom text boxes
def display_report_section(title, content, color):
    """Displays custom stylized box for Objective and Summary."""
    st.markdown(f"### {title}")
    st.markdown(f"""
        <div style="padding: 15px; border-left: 5px solid {color}; background-color: {color}1A; border-radius: 4px; margin-bottom: 20px;">
        <p style="font-size: 0.95rem; line-height: 1.5; margin: 0;">{content}</p>
        </div>
    """, unsafe_allow_html=True)

# --- Page 1: Distribution of Sleep & Stress Factors ---

def page_1_distribution(data):
    st.title("Page 1: Distribution of Sleep & Stress Factors by Demographics")

    # Objective Statement
    display_report_section("Objective Statement", 
                     "This page explores the distribution of key sleep and stress factors among students, specifically focusing on how these factors vary across different years of study and genders.", 
                     "#10B981") # Green

    # Summary Box
    display_report_section("Summary Box (100–150 words)", 
                     """
                     The initial demographic analysis reveals several key distinctions in student well-being. The stacked bar chart shows that **Academic Stress is highest among students in their third and fourth years of study**, indicating increasing pressure as academic programs progress. The box plot confirms a slight but notable difference in average sleep hours, with **female students reporting a marginally lower median sleep duration** than their male counterparts. Crucially, the final visualization demonstrates a powerful correlation: students who rate their sleep quality as 'Very Poor' are overwhelmingly concentrated in the 'Poor' or 'Below Average' academic performance categories. This initial distribution analysis establishes a baseline correlation, linking poor sleep and high stress to lower academic ratings across the student body. (124 words)
                     """, 
                     "#3B82F6") # Blue
    
    st.markdown("---")
    st.subheader("Key Visualizations (3 Plots)")
    
    col1, col2 = st.columns(2)

    with col1:
        st.caption("Visualization 1: Academic Stress Levels by Year of Study (Stacked Bar)")
        # Stacked Bar Chart – Stress Levels by Year of Study (Converted to Plotly)
        stress_year_crosstab = pd.crosstab(data['Year_of_Study'], data['Academic_Stress'], normalize='index').mul(100)
        stress_year_crosstab = stress_year_crosstab.reindex(columns=['Very Low', 'Low', 'Moderate', 'High', 'Very High'])

        fig1 = px.bar(stress_year_crosstab, 
                      y=stress_year_crosstab.index, 
                      x=stress_year_crosstab.columns, 
                      orientation='h',
                      title='Academic Stress Levels by Year of Study',
                      labels={'value': 'Proportion (%)', 'Year_of_Study': 'Year of Study'},
                      color_discrete_sequence=px.colors.sequential.Inferno_r) # Using a sequential theme similar to 'flare'

        fig1.update_layout(height=400, legend_title='Stress Level', yaxis={'categoryorder':'array', 'categoryarray':['First Year', 'Second Year', 'Third Year', 'Fourth Year', 'Postgraduate']})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.caption("Visualization 2: Average Sleep Hours by Gender (Box Plot)")
        # Box Plot – Sleep Hours by Gender (Converted to Plotly)
        fig2 = px.box(data, 
                      x='Gender', 
                      y='Sleep_Hours', 
                      title='Average Sleep Hours by Gender',
                      category_orders={"Gender": ['Male', 'Female']},
                      labels={'Sleep_Hours': 'Average Sleep Hours'},
                      color='Gender',
                      color_discrete_sequence=['#FF7F0E', '#1F77B4']) # Similar to flare hues
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.caption("Visualization 3: Sleep Quality vs Academic Performance (Stacked Bar)")
    # Stacked Bar Chart - Sleep Quality vs Academic Performance (Converted to Plotly)
    cross_tab = pd.crosstab(data['Sleep_Quality'], data['Academic_Performance_Rating'], normalize='index').mul(100)
    # Define order for plotting
    sleep_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent']
    performance_order = ['Poor', 'Below Average', 'Average', 'Good', 'Excellent']
    
    cross_tab = cross_tab.reindex(index=sleep_order, columns=performance_order)

    fig3 = px.bar(cross_tab, 
                  x=cross_tab.index, 
                  y=cross_tab.columns, 
                  title='Relationship between Sleep Quality and Academic Performance',
                  labels={'value': 'Proportion (%)', 'Sleep_Quality': 'Sleep Quality'},
                  color_discrete_sequence=px.colors.sequential.Inferno_r)

    fig3.update_layout(height=500, xaxis={'categoryorder':'array', 'categoryarray':sleep_order}, legend_title='Academic Rating')
    st.plotly_chart(fig3, use_container_width=True)


# --- Page 2: Lifestyle Behaviors and Sleep Quality ---

def page_2_lifestyle_impact(data):
    st.title("Page 2: Lifestyle Behaviors and Overall Sleep Quality")

    # Objective Statement
    display_report_section("Objective Statement", 
                     "This page analyzes the relationship between common student lifestyle behaviors—including caffeine consumption, electronic device usage before sleep, and physical activity—and various indicators of overall sleep quality and sleep disruption.", 
                     "#10B981")

    # Summary Box
    display_report_section("Summary Box (100–150 words)", 
                     """
                     The correlation heatmap confirms that **electronic device use before sleep is the strongest behavioral factor** linked to both 'Difficulty falling asleep' and 'Nighttime awakenings'. The correlation coefficient for device use is notably higher than for caffeine consumption or physical activity. The sleep hours vs. device use density plot further visualizes this, showing the highest concentration of short sleepers (4-5 hours) are also those who use devices 'Often' or 'Every night'. Interestingly, the grouped bar chart on caffeine frequency shows that even moderate caffeine users report significantly poorer sleep quality than those who never consume it. These findings underscore the need for targeted sleep hygiene interventions focused on managing evening screen time and reducing regular caffeine dependence. (120 words)
                     """, 
                     "#3B82F6")
    
    st.markdown("---")
    st.subheader("Key Visualizations (3 Plots)")

    # Prepare data for heatmap (copied structure from Colab)
    behavior_sleep_df = data[['Difficulty_Falling_Asleep', 'Nighttime_Awakenings', 'Sleep_Quality',
                              'Device_Use_Before_Sleep', 'Caffeine_Consumption', 'Physical_Activity']].copy()
    
    # Factorize columns for numeric correlation calculation
    for col in behavior_sleep_df.columns:
        behavior_sleep_df[col], _ = pd.factorize(behavior_sleep_df[col])

    correlation_matrix = behavior_sleep_df.corr()

    # Visualization 1: Correlation Heatmap
    st.caption("Visualization 1: Correlation Matrix of Behaviors and Sleep Issues (Heatmap)")
    fig1 = px.imshow(correlation_matrix,
                     text_auto=".2f",
                     aspect="auto",
                     color_continuous_scale=px.colors.sequential.Inferno_r,
                     title='Correlation Matrix of Behaviors and Sleep Issues')
    fig1.update_xaxes(side="top")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Visualization 2 & 3 Side by Side
    col1, col2 = st.columns(2)

    with col1:
        st.caption("Visualization 2: Average Sleep Hours vs Device Use (Density Heatmap)")
        # Prepare data for the 2nd heatmap (Density Plot, Converted to Plotly)
        sleep_hour_mapping = {'Less than 4 hours': 3, '4-5 hours': 4.5, '5-6 hours': 5.5,
                              '6-7 hours': 6.5, '7-8 hours': 7.5, 'More than 8 hours': 9} 
        device_use_mapping = {'Never': 0, 'Rarely (1-2 times a week)': 1.5, 'Sometimes (3-4 times a week)': 3.5,
                              'Often (5-6 times a week)': 5.5, 'Every night': 7}
        
        heatmap_data = data.pivot_table(index='Sleep_Hours',
                                        columns='Device_Use_Before_Sleep',
                                        aggfunc='size', fill_value=0)
        
        # Reorder based on numeric mappings
        heatmap_data_reordered = heatmap_data.reindex(index=sleep_hour_mapping.keys(), columns=device_use_mapping.keys()).fillna(0)

        fig2 = px.imshow(heatmap_data_reordered,
                         text_auto=True,
                         aspect="auto",
                         color_continuous_scale='tempo',
                         title='Density of Observations: Sleep Hours vs. Electronic Device Use')
        fig2.update_xaxes(side="top", title="Electronic Device Use Before Sleep")
        fig2.update_yaxes(title="Average Hours of Sleep")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.caption("Visualization 3: Sleep Quality by Caffeine Frequency (Grouped Bar)")
        # Grouped Bar Chart – Sleep Quality by Caffeine Frequency (Converted to Plotly)
        caffeine_sleep_crosstab = pd.crosstab(data['Caffeine_Consumption'], data['Sleep_Quality'], normalize='index').mul(100)
        
        caffeine_order = ['Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)', 'Often (5-6 times a week)', 'Every day']
        sleep_quality_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent']

        # Ensure index and columns are ordered
        caffeine_sleep_crosstab = caffeine_sleep_crosstab.reindex(index=caffeine_order, columns=sleep_quality_order)

        fig3 = px.bar(caffeine_sleep_crosstab, 
                      x=caffeine_sleep_crosstab.index, 
                      y=caffeine_sleep_crosstab.columns, 
                      title='Sleep Quality Ratings by Caffeine Consumption Frequency',
                      labels={'value': 'Proportion (%)', 'Caffeine_Consumption': 'Caffeine Consumption Frequency'},
                      color_discrete_sequence=px.colors.sequential.Inferno_r)

        fig3.update_layout(height=400, xaxis={'categoryorder':'array', 'categoryarray':caffeine_order}, legend_title='Sleep Quality')
        st.plotly_chart(fig3, use_container_width=True)


# --- Page 3: Impact on Concentration, Fatigue, and Performance ---

def page_3_academic_impact(data):
    st.title("Page 3: Impact on Concentration, Fatigue, and Academic Performance")

    # Objective Statement
    display_report_section("Objective Statement", 
                     "This page investigates the causal impact of self-reported sleep-related issues on the student's daily functional metrics, specifically focusing on concentration levels, frequency of fatigue, and their cumulative effect on academic performance.", 
                     "#10B981")

    # Summary Box
    display_report_section("Summary Box (100–150 words)", 
                     """
                     The visualizations here quantify the significant cost of poor sleep on daily academic functioning. The box plot shows a clear and progressive decline in median academic performance rating as the **Impact of insufficient sleep on assignment completion** shifts from 'No impact' to 'Severe impact'. The most compelling finding comes from the concentration vs. fatigue heatmap: the lowest average academic performance scores are clustered in the areas where students report concentrating difficulty and fatigue 'Often' or 'Always'. Finally, the violin plot reinforces this, showing the highest median and narrowest distribution of 'Excellent' performance only among students who 'Never' or 'Rarely' struggle to concentrate due to sleep loss. These results prove that sleep is a direct, performance-limiting factor. (125 words)
                     """, 
                     "#3B82F6")
    
    st.markdown("---")
    st.subheader("Key Visualizations (3 Plots)")
    
    col1, col2 = st.columns(2)

    # Define order for categorical axes
    impact_order = ['No impact', 'Minor impact', 'Moderate impact', 'Major impact', 'Severe impact']
    frequency_order = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']

    with col1:
        st.caption("Visualization 1: Academic Performance by Assignment Impact (Box Plot)")
        # Box Plot: Performance grouped by Assignment Impact (Converted to Plotly)
        fig1 = px.box(data, 
                      x='Assignment_Impact', 
                      y='Academic_Performance_Numeric', 
                      title='Academic Performance by Impact of Insufficient Sleep on Assignments',
                      category_orders={"Assignment_Impact": impact_order},
                      labels={'Academic_Performance_Numeric': 'Academic Performance (1=Poor, 5=Excellent)', 'Assignment_Impact': 'Impact on Assignment Completion'},
                      color='Assignment_Impact',
                      color_discrete_sequence=px.colors.sequential.Inferno_r)
        fig1.update_layout(height=450, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.caption("Visualization 2: Performance by Difficulty Concentrating (Violin Plot)")
        # Violin Plot - Academic Performance by Difficulty Concentrating (Converted to Plotly)
        fig2 = px.violin(data, 
                         x='Difficulty_Concentrating', 
                         y='Academic_Performance_Numeric', 
                         title='Distribution of Academic Performance by Difficulty Concentrating',
                         category_orders={"Difficulty_Concentrating": frequency_order},
                         labels={'Academic_Performance_Numeric': 'Academic Performance (1=Poor, 5=Excellent)', 'Difficulty_Concentrating': 'Difficulty Concentrating Frequency'},
                         color='Difficulty_Concentrating',
                         color_discrete_sequence=px.colors.sequential.Inferno_r)
        fig2.update_layout(height=450, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.caption("Visualization 3: Average Performance by Fatigue and Concentration (Heatmap)")
    # Heatmap: Performance by Fatigue and Concentration (Converted to Plotly)
    
    heatmap_data_performance = data.pivot_table(index='Difficulty_Concentrating',
                                                columns='Fatigue_Frequency',
                                                values='Academic_Performance_Numeric',
                                                aggfunc='mean')
    
    # Reorder index and columns using the categorical lists
    heatmap_data_performance = heatmap_data_performance.reindex(index=frequency_order, columns=frequency_order)

    fig3 = px.imshow(heatmap_data_performance,
                     text_auto=".2f",
                     aspect="auto",
                     color_continuous_scale=px.colors.sequential.Inferno_r,
                     title='Average Academic Performance by Fatigue and Concentration Difficulty')
    fig3.update_xaxes(side="top", title="Fatigue Frequency")
    fig3.update_yaxes(title="Concentration Difficulty Frequency")
    st.plotly_chart(fig3, use_container_width=True)


# --- Main Application Logic ---

def main():
    st.sidebar.title("Dashboard Navigation")
    
    # Use radio buttons for page selection
    pages = {
        "Page 1: Sleep/Stress Distribution": page_1_distribution,
        "Page 2: Lifestyle Behaviors Impact": page_2_lifestyle_impact,
        "Page 3: Functional & Academic Impact": page_3_academic_impact
    }
    
    selection = st.sidebar.radio("Go to:", list(pages.keys()))
    
    # Call the selected page function
    page = pages[selection]
    page(df)

if __name__ == "__main__":
    main()
