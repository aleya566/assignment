import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    st.title("💤 Objective 2: Lifestyle Habits and Sleep Impact")

    url = "https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv"
    df = pd.read_csv(url)

    st.subheader("Caffeine Consumption vs Sleep Quality")
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x='12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?', hue='6. How would you rate the overall quality of your sleep?')
    plt.xticks(rotation=45)
    plt.xlabel("Caffeine Consumption Frequency")
    plt.ylabel("Count")
    plt.title("Impact of Caffeine on Sleep Quality")
    st.pyplot(plt)

    st.write("This visualization explores how caffeine consumption frequency correlates with students’ perceived sleep quality.")

if __name__ == "__main__":
    main()
