# Function to analyze mood using OpenAI GPT-3.5
import os
from uagents import Agent, Model, Context, Bureau
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import asyncio
import logging
import openai
from recordAudio import record_audio  # Import the recording function

from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")  # Fetch OpenAI API key from environment variable
client = OpenAI()


async def analyze_mood(transcriptions):
    try:
        # Create a completion request using the chat completion API
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Correct model name
                messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": "Analyze the following text from a daily journal entry and determine the mood of the user: in one word - stressed, happy, sad, excited, neutral"},
                            {"role": "user", "content": f"{transcriptions}"}
                        ]
        )
        # Extract and return the mood from the response
        mood = completion.choices[0].message.content
        return mood
    except Exception as e:
        return f"Error during mood analysis: {str(e)}"

# Function to generate a follow-up question based on the detected mood
def generate_follow_up_question(mood):
    follow_up_questions = {
        "stressed": "It seems like you're feeling stressed. Would you like to share more about what's causing it?",
        "happy": "You seem happy! What made you feel this way today?",
        "sad": "I'm sorry to hear you're feeling sad. Would you like to talk more about what's on your mind?",
        "excited": "That's great! What are you most excited about?",
        "neutral": "Is there anything else you'd like to add about how you're feeling today?"
    }

    # Match the mood to a follow-up question, default to neutral if mood is unknown
    return follow_up_questions.get(mood.lower(), "Is there anything else you'd like to share today?")

def summarize_journal(transcriptions):
    try:
        # Create a completion request using the chat completion API
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Correct model name
                messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": "This is the journal entry of a person, combine it and structure it in a better way in terms of language."},
                            {"role": "user", "content": f"{transcriptions}"}
                        ]
        )
        summary = completion.choices[0].message.content
        return summary
    except Exception as e:
        return f"Error during summarization: {str(e)}"

