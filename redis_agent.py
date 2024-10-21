from uagents import Agent, Model, Context
# from recordAudio import transcribe_audio
from uagents.setup import fund_agent_if_low
import datetime
from datetime import date
import openai_function
from datetime import datetime
from typing import List


class RedisMessage(Model):
    summary:str
    date : date
    mood : str 
    transcript_list : List[str]

# Create the transcription agent
redis_agent = Agent(
    name="redis_agent",
    seed="redis_agent_seed",
    port=8006,
    endpoint=['http://localhost:8006/submit']
)

fund_agent_if_low(redis_agent.wallet.address())
print(f"redis Agent Address: {redis_agent.address}")

# Handler for incoming audio file messages in the transcription agent
@redis_agent.on_message(model=RedisMessage)
async def handle_audio_file_message(ctx: Context, sender: str, msg: RedisMessage):
    print(f"[Redis Agent] Received audio file path from {sender}")
    print(f'q1 - {msg.transcript_list[0]}')
    print(f'q2 - {msg.transcript_list[1]}')
    print(f'mood - {msg.mood}')
    print(f'date - {msg.date}')
    print(f'summary - {msg.summary}')

# Print the transcription agent's addresss
print(f"Redis Agent Address: {redis_agent.address}")


if __name__ == "__main__":
    redis_agent.run()