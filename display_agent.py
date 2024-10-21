from uagents import Agent, Model, Context
import openai
from openai import OpenAI
from uagents.setup import fund_agent_if_low
import openai_function
import datetime
from datetime import datetime
from typing import List

# Define the message models
class TranscriptionMessage(Model):
    transcription: str
    idx: int

class SummaryMessage(Model):
    summary : str
    mood : str
    transcript_list : List[str]

class RedisMessage(Model):
    summary:str
    date : datetime
    mood : str
# Create the display agent
display_agent = Agent(
    name="display_agent",
    seed="display_agent_seed",
    port=8004,
    endpoint=['http://localhost:8004/submit']
)

fund_agent_if_low(display_agent.wallet.address())

# OpenAI Client
client = OpenAI()

transcriptions = []

# Handler for incoming transcription messages in the display agent
@display_agent.on_message(model=TranscriptionMessage)
async def handle_transcription_message(ctx: Context, sender: str, msg: TranscriptionMessage):
    print(f"\n[Display Agent] Received transcription from {sender}")
    print("Transcription:")
    print(msg.transcription)
    # Store the transcription
    transcriptions.append(msg.transcription)

    # Display the transcriptions and analyze mood if necessary
    if len(transcriptions) == 2:  # Assuming there are 2 questions
        combined_transcriptions = " ".join(transcriptions)
        print(f"\nCombined Transcriptions: {combined_transcriptions}")
        mood = await openai_function.analyze_mood(combined_transcriptions)

        print(f"\nOverall Mood Analysis: {mood}")
        # Generate follow-up question based on mood
        follow_up_question = openai_function.generate_follow_up_question(mood)
        print(f"\nFollow-up Question: {follow_up_question}")
        await ctx.send("agent1qw5ferxutdqu0vd74sln0kll52py8g6f8a6yk4lrws39jpvdedftxr9jlnf", SummaryMessage(summary=combined_transcriptions, mood = mood,transcript_list = transcriptions))
        

# Print the display agent's address
print(f"Display Agent Address: {display_agent.address}")


if __name__ == "__main__":
    display_agent.run()