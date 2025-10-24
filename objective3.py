import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    st.title("📖 Objective 3: Sleep and Academic Performance")

    url = "https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv"
    df = pd.read_csv(url)

    st.subheader("Relationship Between Sleep Quality and Academic Performance")
    plt.figure(figsize=(7, 5))
    sns.boxplot(data=df, x='6. How would you rate the overall quality of your sleep?', y='15. How would you rate your overall academic performance (GPA or grades) in the past semester?')
    plt.xlabel("Sleep Quality")
    plt.ylabel("Academic Performance")
    plt.title("Sleep Quality vs Academic Performance")
    st.pyplot(plt)

    st.write("This chart visualizes how sleep quality may influence students’ academic outcomes.")

if __name__ == "__main__":
    main()
