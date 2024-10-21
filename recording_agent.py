import os
from uagents import Agent, Model, Context
import asyncio
from recordAudio import record_audio
from uagents.setup import fund_agent_if_low
# Define the message models

class RecordAudioMessage(Model):
    question: str
    idx: int
    duration: int

class AudioFileMessage(Model):
    filepath: str
    idx: int

# Create the recording agent
recording_agent = Agent(
    name="recording_agent",
    seed="recording_agent_seed",
    port=8002,
    endpoint=['http://localhost:8002/submit']
)

fund_agent_if_low(recording_agent.wallet.address())

# Handler in the recording agent to record audio
@recording_agent.on_message(model=RecordAudioMessage)
async def handle_record_audio(ctx: Context, sender: str, msg: RecordAudioMessage):
    print(f"\nRecording for Question {msg.idx}: {msg.question}")
    input("Press Enter when you're ready to record...")

    # Record the audio
    filename = f"response_{msg.idx}.wav"
    duration = msg.duration

    # Run the blocking recording in an executor
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, record_audio, duration, filename)

    # Check if the audio file exists
    if not os.path.exists(filename):
        print(f"Audio file {filename} not found.")
        return

    # Send the audio file message to the transcription agent using its address
    await ctx.send("agent1qt9ymdhph4luhj83qajjpgmvz7p7h88ddxjtwchyagvgta3dghdk55jf5zu", AudioFileMessage(filepath=filename, idx=msg.idx))

# Print the recording agent's address
print(f"Recording Agent Address: {recording_agent.address}")


if __name__ == "__main__":
    recording_agent.run()