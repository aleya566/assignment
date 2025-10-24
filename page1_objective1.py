import streamlit as st
import pandas as pd
import plotly.express as px

def page_1_distribution(df):
    st.title("Objective 1: Distribution of Sleep & Stress Factors by Demographics")

    st.markdown("""
    ### Objective Statement
    To explore the distribution of key sleep and stress factors among students across different years of study and genders.
    """)

    # --- Visualization 1: Academic Stress Levels by Year of Study (Stacked Bar) ---
    st.subheader("Visualization 1: Academic Stress Levels by Year of Study")

    stress_year_crosstab = pd.crosstab(
        df['1. What is your year of study?'],
        df['14. How would you describe your stress levels related to academic workload?'],
        normalize='index'
    ) * 100

    # Order columns if applicable
    stress_order = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
    stress_year_crosstab = stress_year_crosstab.reindex(columns=[c for c in stress_order if c in stress_year_crosstab.columns])

    fig1 = px.bar(
        stress_year_crosstab,
        x=stress_year_crosstab.index,
        y=stress_year_crosstab.columns,
        title="Academic Stress Levels by Year of Study",
        labels={'value': 'Proportion (%)', 'index': 'Year of Study'},
        color_discrete_sequence=px.colors.sequential.Inferno_r
    )
    fig1.update_layout(barmode='stack', xaxis_title="Year of Study", yaxis_title="Proportion (%)")
    st.plotly_chart(fig1, use_container_width=True)

    # --- Visualization 2: Average Sleep Hours by Gender (Box Plot) ---
    st.subheader("Visualization 2: Average Sleep Hours by Gender")

    fig2 = px.box(
        df,
        x='2. What is your gender?',
        y='4. On average, how many hours of sleep do you get on a typical day?',
        color='2. What is your gender?',
        category_orders={'2. What is your gender?': ['Male', 'Female']},
        color_discrete_sequence=px.colors.sequential.Inferno_r
    )
    fig2.update_layout(
        title="Average Sleep Hours by Gender",
        xaxis_title="Gender",
        yaxis_title="Average Sleep Hours",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Visualization 3: Relationship between Sleep Quality and Academic Performance (Stacked Bar) ---
    st.subheader("Visualization 3: Sleep Quality vs Academic Performance")

    cross_tab = pd.crosstab(
        df['6. How would you rate the overall quality of your sleep?'],
        df['15. How would you rate your overall academic performance (GPA or grades) in the past semester?'],
        normalize='index'
    ) * 100

    sleep_order = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent']
    performance_order = ['Poor', 'Below Average', 'Average', 'Good', 'Excellent']

    cross_tab = cross_tab.reindex(index=sleep_order, columns=[c for c in performance_order if c in cross_tab.columns])

    fig3 = px.bar(
        cross_tab,
        x=cross_tab.index,
        y=cross_tab.columns,
        title="Relationship between Sleep Quality and Academic Performance",
        labels={'value': 'Proportion (%)', 'index': 'Sleep Quality'},
        color_discrete_sequence=px.colors.sequential.Inferno_r
    )
    fig3.update_layout(barmode='stack', xaxis_title="Sleep Quality", yaxis_title="Proportion (%)")
    st.plotly_chart(fig3, use_container_width=True)
