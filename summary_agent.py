from uagents import Agent, Model, Context
# from recordAudio import transcribe_audio
from uagents.setup import fund_agent_if_low
import datetime
from datetime import date
import openai_function
from datetime import datetime
from typing import List



class SummaryMessage(Model):
    summary : str
    mood : str
    transcript_list : List[str]
   

class RedisMessage(Model):
    summary:str
    date : date
    mood : str 
    transcript_list : List[str]

# Create the transcription agent
summary_agent = Agent(
    name="summary_agent",
    seed="summary_agent_seed",
    port=8005,
    endpoint=['http://localhost:8005/submit']
)

fund_agent_if_low(summary_agent.wallet.address())
print(f"summary Agent Address: {summary_agent.address}")

# Handler for incoming audio file messages in the transcription agent
@summary_agent.on_message(model=SummaryMessage)
async def handle_audio_file_message(ctx: Context, sender: str, msg: SummaryMessage):
    print(f"[Summary Agent] Received a SummaryMessage type from {sender}")

    # Transcribe the audio file
    summary = openai_function.summarize_journal(msg.summary)

    print(f"Summary of today's journal: {summary}")
    await ctx.send("agent1qw30j7c7x2p6evel4jag89tpldtkzql97gz7pr8vlczgzf28ww5nuwy5ngt", RedisMessage(transcript_list = msg.transcript_list, summary=summary, date = date.today(), mood = msg.mood))
        

# Print the transcription agent's addresss
print(f"Summary Agent Address: {summary_agent.address}")


if __name__ == "__main__":
    summary_agent.run()