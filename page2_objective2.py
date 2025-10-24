import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("💤 Objective 2: Lifestyle Habits and Sleep Impact")

    url = "https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv"
    df = pd.read_csv(url)

    st.subheader("☕ Caffeine Consumption vs Sleep Quality")

    fig = px.histogram(
        df,
        x='12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?',
        color='6. How would you rate the overall quality of your sleep?',
        barmode='group',
        title="Impact of Caffeine Consumption on Sleep Quality",
        labels={
            'x': 'Caffeine Consumption Frequency',
            'color': 'Sleep Quality'
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(xaxis_title="Caffeine Consumption", yaxis_title="Number of Students", bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)

    st.write("This visualization shows how caffeine consumption frequency may affect the perceived sleep quality among students.")

if __name__ == "__main__":
    main()
