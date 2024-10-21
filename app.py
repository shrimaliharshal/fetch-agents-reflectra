import streamlit as st
import requests
import os
from datetime import date
from recordAudio import record_audio

# Set up the questions (same as in your sender_agent)
JOURNALING_QUESTIONS = [
    "How was your day?",
    "What challenges did you face today?"
]

# Display questions to the user
st.title("AI Journaling Assistant")

# Use state to manage current question index
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

# Display the current question
question = JOURNALING_QUESTIONS[st.session_state.question_index]
st.subheader(f"Question {st.session_state.question_index + 1}: {question}")

# Define the record button
if st.button("Start Recording"):
    # Record the audio when the button is pressed
    filename = f"response_{st.session_state.question_index + 1}.wav"
    record_audio(duration=5, filename=filename)

    # Upload the recorded file to the backend agent (for simulation)
    st.write(f"Recording saved as {filename}.")
    st.session_state.recorded = True

# Button to move to the next question
if st.session_state.get('recorded', False):
    if st.button("Next Question"):
        # Move to the next question
        if st.session_state.question_index + 1 < len(JOURNALING_QUESTIONS):
            st.session_state.question_index += 1
            st.session_state.recorded = False
        else:
            st.write("All questions completed.")

# Display journal summary and mood from Redis agent
if st.session_state.get('recorded', False) and st.session_state.question_index + 1 == len(JOURNALING_QUESTIONS):
    st.subheader("Fetching your journal summary...")

    # Call the Redis agent to get the summary and mood
    response = requests.get("http://localhost:8006/get_journal")  # Replace with the correct agent endpoint

    if response.status_code == 200:
        data = response.json()
        st.write(f"Date: {data['date']}")
        st.write(f"Mood: {data['mood']}")
        st.write(f"Summary: {data['summary']}")
    else:
        st.write("Failed to fetch journal summary.")
