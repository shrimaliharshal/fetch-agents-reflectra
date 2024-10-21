from uagents import Agent, Model, Context
from recordAudio import transcribe_audio
from uagents.setup import fund_agent_if_low

# Define the message models
class AudioFileMessage(Model):
    filepath: str
    idx: int

class TranscriptionMessage(Model):
    transcription: str
    idx: int

# Create the transcription agent
transcription_agent = Agent(
    name="transcription_agent",
    seed="transcription_agent_seed",
    port=8003,
    endpoint=['http://localhost:8003/submit']
)

fund_agent_if_low(transcription_agent.wallet.address())

# Handler for incoming audio file messages in the transcription agent
@transcription_agent.on_message(model=AudioFileMessage)
async def handle_audio_file_message(ctx: Context, sender: str, msg: AudioFileMessage):
    print(f"[Transcription Agent] Received audio file path from {sender}")

    # Transcribe the audio file
    transcription = await transcribe_audio(msg.filepath)

    # Send the transcription to the display agent using its address
    await ctx.send("agent1q278jzg45mrcqm5g5lkgyk66j7cs9nsvxf6xu8u0q0sedln3w27ngmua7se", TranscriptionMessage(transcription=transcription, idx=msg.idx))

# Print the transcription agent's address
print(f"Transcription Agent Address: {transcription_agent.address}")


if __name__ == "__main__":
    transcription_agent.run()