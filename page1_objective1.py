import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("🎯 Objective 1: Distribution of Student Sleep Patterns")

    # Load data
    url = "https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv"
    df = pd.read_csv(url)

    # Bar chart for sleep hours
    st.subheader("🛌 Average Sleep Hours Distribution")
    sleep_counts = df['4. On average, how many hours of sleep do you get on a typical day?'].value_counts().sort_index()

    fig = px.bar(
        x=sleep_counts.index,
        y=sleep_counts.values,
        labels={'x': 'Average Hours of Sleep', 'y': 'Number of Students'},
        text=sleep_counts.values,
        color=sleep_counts.values,
        color_continuous_scale='Blues',
        title="Distribution of Average Sleep Hours Among Students"
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    st.write("This chart displays how many hours students typically sleep per night, providing an overview of general sleep habits.")

if __name__ == "__main__":
    main()
