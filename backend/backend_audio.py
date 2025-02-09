import openai

# For the API key
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        print(transcript)
        return transcript.text  # Adjusted to match new API response format
    
def detect_speech_needs_help(transcript):
    transcript = transcript.lower()
    return "help" in transcript or "emergency" in transcript or "danger" in transcript

def detect_speech_needs_help_custom_word(transcript, keyword):
    transcript = transcript.lower()
    return keyword in transcript # Check for custom keyword


if __name__ == "__main__":
    audio_path = r"data\Recording (3).m4a"
    transcript = transcribe_audio(audio_path)

