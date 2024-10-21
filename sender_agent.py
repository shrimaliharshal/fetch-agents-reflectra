from uagents import Agent, Model, Context
from uagents.setup import fund_agent_if_low

# Define the message models
class StartRecordingMessage(Model):
    question: str
    idx: int

# Define the message models
class RecordAudioMessage(Model):
    question: str
    idx: int
    duration: int

# Create the sender agent
sender_agent = Agent(
    name="sender_agent",
    seed="sender_agent_seed",
    port=8001,
    endpoint=['http://localhost:8001/submit']
)

fund_agent_if_low(sender_agent.wallet.address())

JOURNALING_QUESTIONS = [
    "How was your day?",
    "What challenges did you face today?"
]

journaling_started = False

# Handler in the sender agent to start the journaling process
@sender_agent.on_interval(period=30.0)  # Set the interval to start asking questions
async def start_journaling(ctx: Context):
    global journaling_started
    if journaling_started:
        return  # Exit if the journaling has already started
    journaling_started = True

    for idx, question in enumerate(JOURNALING_QUESTIONS, start=1):
        print(f"Sending question {idx}: {question}")
        # Send a RecordAudioMessage to the recording agent
        await ctx.send("agent1qgr68mdea9paflx0te4ljyztjfxaj5fxgj6rgs55pk4nhfpc8ru7y3t8lav", RecordAudioMessage(question=question, idx=idx, duration=5))

# Print the sender agent's address
print(f"Sender Agent Address: {sender_agent.address}")


if __name__ == "__main__":
    sender_agent.run()