import sounddevice as sd
from scipy.io.wavfile import write
import time

import os
from uagents import Agent, Model, Context, Bureau
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import asyncio
import logging
import openai


DEEPGRAM_API_KEY = 'use-your-key'
def record_audio(duration=5, filename='recorded_audio.wav', fs=44100):
    """
    Records audio from the microphone and saves it to a WAV file.

    Args:
        duration (int): Duration of the recording in seconds.
        filename (str): The filename to save the recording.
        fs (int): Sampling frequency (samples per second).
    """
    print(f"Recording for {duration} seconds...")
    # Record audio for the given duration
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")

    # Save the recording to a WAV file
    write(filename, fs, recording)
    print(f"Audio saved to {filename}.")




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
    duration = int(input("Enter recording duration in seconds: "))
    filename = input("Enter filename to save recording (e.g., 'recorded_audio.wav'): ") or 'recorded_audio.wav'
    record_audio(duration=duration, filename=filename)
