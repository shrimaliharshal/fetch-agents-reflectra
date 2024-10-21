import os
from uagents import Agent, Model, Context, Bureau
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import logging
import recordAudio


# Replace with your actual Deepgram API key
DEEPGRAM_API_KEY = 'use your key'

# Ensure the API key is provided
if not DEEPGRAM_API_KEY:
    raise ValueError("Please set your Deepgram API key in the DEEPGRAM_API_KEY variable.")

# Define the message models
class AudioFileMessage(Model):
    filepath: str

class TranscriptionMessage(Model):
    transcription: str

# Create the Bureau to manage the agents
bureau = Bureau()

# Create the sender agent
sender_agent = Agent(
    name="sender_agent",
    seed="sender_agent_seed",
)

# Create the transcription agent
transcription_agent = Agent(
    name="transcription_agent",
    seed="transcription_agent_seed",
)

# Create the display agent
display_agent = Agent(
    name="display_agent",
    seed="display_agent_seed",
)

# Add agents to the Bureau
bureau.add(sender_agent)
bureau.add(transcription_agent)
bureau.add(display_agent)

# Add a flag to control message sending
message_sent = False

# Sender agent sends the message after startup using on_interval decorator
@sender_agent.on_interval(period=1.0)
async def send_audio_file_message(ctx: Context):
    global message_sent
    if message_sent:
        return  # Exit if the message has already been sent

    # Path to the audio file to transcribe
    #recordAudio.record_audio(duration=10, filename=check.wav)
    AUDIO_FILE = "check.wav"

    # Check if the audio file exists
    if not os.path.exists(AUDIO_FILE):
        print(f"Audio file {AUDIO_FILE} not found.")
        #await bureau.stop()
        return

    # Create an AudioFileMessage
    audio_message = AudioFileMessage(filepath=AUDIO_FILE)

    # Sender agent sends the audio file message to the transcription agent
    await ctx.send(transcription_agent.address, audio_message)
    print(f"[Sender Agent] Sent audio file path to {transcription_agent.address}")

    # Set the flag to True to prevent future executions
    message_sent = True

# Handler for incoming audio file messages in the transcription agent
@transcription_agent.on_message(model=AudioFileMessage)
async def handle_audio_file_message(ctx: Context, sender: str, msg: AudioFileMessage):
    print(f"[Transcription Agent] Received audio file path from {sender}")

    # Transcribe the audio file
    transcription = await transcribe_audio(msg.filepath)

    # Send the transcription to the display agent
    response = TranscriptionMessage(transcription=transcription)
    await ctx.send(display_agent.address, response)
    print(f"[Transcription Agent] Sent transcription to {display_agent.address}")

# Handler for incoming transcription messages in the display agent
@display_agent.on_message(model=TranscriptionMessage)
async def handle_transcription_message(ctx: Context, sender: str, msg: TranscriptionMessage):
    print(f"[Display Agent] Received transcription from {sender}")
    print("Transcription:")
    print(msg.transcription)
    # Stop the Bureau after displaying the transcription
    #await bureau.stop()

# Function to transcribe audio using Deepgram
async def transcribe_audio(audio_filepath):
    try:
        # Initialize the Deepgram client
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        # Read the audio file
        with open(audio_filepath, 'rb') as audio_file:
            buffer_data = audio_file.read()

        # Prepare the payload for transcription
        payload: FileSource = {
            "buffer": buffer_data,
        }

        # Configure transcription options
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # Transcribe the audio file
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # Extract the transcription from the response
        transcription = response.results.channels[0].alternatives[0].transcript

        return transcription

    except Exception as e:
        print(f"Exception during transcription: {e}")
        return "Transcription failed."

if __name__ == '__main__':
    # Run the Bureau (this will block until bureau.stop() is called)
    bureau.run()

logging.basicConfig(level=logging.ERROR)
