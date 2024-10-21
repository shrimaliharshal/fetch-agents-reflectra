import openai
import os

from openai import OpenAI

# Automatically gets API Key from environment variable OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Journal entry
transcript = "I had a really busy day today, and it left me feeling a bit overwhelmed, but I also felt accomplished after finishing all my tasks."

# Create a completion request using the chat completion API
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",  # Correct model name
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Analyze the following text from a daily journal entry and determine the mood of the user: in stressed, happy, sad, excited, neutral"},
    {"role": "user", "content": f"{transcript}"}
  ]
)
print(completion.choices[0].message.content)

# Extract and print the mood from the response
mood = completion.choices[0].message.content
# print(f"Detected Mood: {mood}")
# print(mood)
