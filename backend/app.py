from flask import Flask, jsonify, send_file, request, session
from flask_cors import CORS

# for the backend functions
from backend_audio import transcribe_audio, detect_speech_needs_help
from twil_guy import send_emergency_text

# for the API key
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()
app.secret_key = os.getenv("OPENAI_API_KEY")

@app.route('/gps', methods=['POST'])
def gps():
    data = request.get_json()
    session['gps'] = data
    return jsonify(message="GPS coordinates stored successfully")

@app.route('/alert', methods=['GET'])
def alert():
    return jsonify(message="successful! the authorities have been contacted")

@app.route("/process", methods=["POST"])
def process_audio():
    """Receives audio, transcribes, detects emergency, and sends alert if needed."""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio_file = request.files["audio"]
    audio_path = f"uploads/{audio_file.filename}"
    audio_file.save(audio_path)

    # Transcribe the audio
    transcript = transcribe_audio(audio_path)
    print(f"Transcript: {transcript}")

    # Check if it's an emergency
    emergency_detected = detect_speech_needs_help(transcript)

    # Send SMS if emergency is detected
    if emergency_detected:
        send_emergency_text(["+919082835960"], "🚨 Emergency Alert! Immediate action required.")

    return jsonify({"transcript": transcript, "emergency_detected": emergency_detected})

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
