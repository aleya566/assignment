import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("🎯 Objective 1: Distribution of Student Sleep Patterns")

    url = "https://raw.githubusercontent.com/aleya566/assignment/refs/heads/main/Student%20Insomnia%20and%20Educational%20Outcomes%20Dataset.csv"
    df = pd.read_csv(url)

    st.subheader("Sleep Duration Distribution")
    plt.figure(figsize=(8, 5))
    df['4. On average, how many hours of sleep do you get on a typical day?'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.xlabel("Hours of Sleep")
    plt.ylabel("Number of Students")
    plt.title("Distribution of Average Sleep Hours")
    st.pyplot(plt)

    st.write("This chart shows how many hours students typically sleep per night. It helps identify common sleep duration trends.")

if __name__ == "__main__":
    main()
