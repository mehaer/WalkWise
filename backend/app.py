from flask import Flask, jsonify, send_file, request, session
from flask_cors import CORS

# for the backend functions
from backend_audio import transcribe_audio, detect_speech_needs_help
from twil_guy import send_emergency_text
from backend_audio_emotion import analyze_emotion, extract_audio_features

# for the API key
import os
from dotenv import load_dotenv

# for mongodb
from config import audio_collection

app = Flask(__name__)
CORS(app)

# In-memory storage for demonstration purposes
locations = []
load_dotenv()
app.secret_key = os.getenv("OPENAI_API_KEY")

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Save the location data
    locations.append({'latitude': latitude, 'longitude': longitude})
    
    return jsonify(message=f"Successful! The authorities have been contacted. Location: ({latitude}, {longitude})")

@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify(locations)

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
    
    # MongoDB: Insert audio metadata
    audio_metadata = {
        "endpoint": "process_audio",
        "filename": audio_file.filename,
        "emergency_detected": emergency_detected,
    }
    audio_collection.insert_one(audio_metadata)
    print(f"Audio file saved: {audio_path}") 


    # Send SMS if emergency is detected
    # if emergency_detected:
    #     send_emergency_text(["+919082835960"], "Emergency Alert! Immediate action required.")

    return jsonify({"transcript": transcript, "emergency_detected": emergency_detected})

@app.route("/sentiment", methods=["POST"])
def sentiment_audio():
    """Receives audio, transcribes, and analyzes sentiment (fear detection)."""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    # Save the received audio file
    audio_file = request.files["audio"]
    audio_path = f"uploads/{audio_file.filename}"
    os.makedirs("uploads", exist_ok=True)  # Ensure upload directory exists
    audio_file.save(audio_path)

    # Analyze emotion from voice
    emotion = analyze_emotion(audio_path)
    audio_features = extract_audio_features(audio_path)

    # Classify emergency based on emotion analysis
    emergency_detected = emotion == "fear"  # Emergency if fear is detected
    
    # MongoDB: Insert audio metadata
    audio_metadata = {
        "filename": audio_file.filename,
        "emotion": emotion,
        "emergency_detected": emergency_detected,
        "features": audio_features
    }
    audio_collection.insert_one(audio_metadata)
    print(f"Audio file saved: {audio_path}")

    # Send SMS if emergency is detected
    # if emergency_detected:
    #     send_emergency_text(["+919082835960"], "🚨 Emergency Alert! Immediate action required due to voice distress.")

    return jsonify({
        "emotion": emotion,
        "emergency_detected": emergency_detected,
        "audio_features": audio_features
    })

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
