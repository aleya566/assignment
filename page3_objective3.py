import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("📖 Objective 3: Sleep and Academic Performance")

    url = "https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv"
    df = pd.read_csv(url)

    st.subheader("📊 Relationship Between Sleep Quality and Academic Performance")

    fig = px.box(
        df,
        x='6. How would you rate the overall quality of your sleep?',
        y='15. How would you rate your overall academic performance (GPA or grades) in the past semester?',
        color='6. How would you rate the overall quality of your sleep?',
        title="Sleep Quality vs Academic Performance",
        labels={
            'x': 'Sleep Quality',
            'y': 'Academic Performance Rating'
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("This boxplot highlights how different levels of sleep quality are associated with academic performance among students.")

if __name__ == "__main__":
    main()
