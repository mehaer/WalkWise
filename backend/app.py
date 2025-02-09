from flask import Flask, jsonify, send_file, request, session
from flask_cors import CORS

# for the backend functions
from backend_audio import transcribe_audio, detect_speech_needs_help, detect_speech_needs_help_custom_word
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
    
    message = "No emergency detected."
    
    if emergency_detected:
        message = "Emergency Alert! Contacted the nearest authorities through Twilio."
    

    return jsonify({"transcript": transcript, "emergency_detected": emergency_detected, "message": message})

@app.route("/process_custom", methods=["POST"])
def process_audio_custom():
    """Receives audio & keyword, transcribes, checks for emergency, and stores metadata in MongoDB."""
    if "audio" not in request.files or "keyword" not in request.form:
        return jsonify({"error": "Audio file and keyword are required"}), 400

    # Retrieve file and keyword
    audio_file = request.files["audio"]
    keyword = request.form["keyword"].strip().lower()  # Convert keyword to lowercase for case-insensitive match

    # Save audio locally for processing
    audio_path = f"uploads/{audio_file.filename}"
    os.makedirs("uploads", exist_ok=True)
    audio_file.save(audio_path)

    # Transcribe the audio
    transcript = transcribe_audio(audio_path)
    print(f"Transcript: {transcript}")

    # Check if it's an emergency based on the provided keyword
    emergency_detected = detect_speech_needs_help_custom_word(transcript, keyword)

    # MongoDB: Store audio metadata
    audio_metadata = {
        "filename": audio_file.filename,
        "transcript": transcript,
        "emergency_detected": emergency_detected,
        "keyword_used": keyword
    }
    audio_collection.insert_one(audio_metadata)

    print(f"Audio file saved: {audio_path}")

    # Send SMS if emergency is detected
    # if emergency_detected:
    #     send_emergency_text(["+919082835960"], f" Emergency Alert! Keyword '{keyword}' detected in speech.")
    
    message = "No emergency detected."
    
    if emergency_detected:
        message = f"Emergency Alert! Keyword '{keyword}' detected in speech. Contacted the nearest authorities through Twilio."

    return jsonify({
        "transcript": transcript,
        "emergency_detected": emergency_detected,
        "keyword_used": keyword,
        "message": message
    })
    

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
    
    message = "No emergency detected."
    
    if emergency_detected:
        message = "Emergency Alert! Contacted the nearest authorities through Twilio."


    return jsonify({
        "emotion": emotion,
        "emergency_detected": emergency_detected,
        "audio_features": audio_features,
        "message": message
    })
    
@app.route("/audio_metadata", methods=["GET"])
def get_audio_metadata():
    """Fetch all stored audio metadata from MongoDB."""
    audio_records = list(audio_collection.find({}, {"_id": 0}))  # Exclude MongoDB `_id`
    return jsonify(audio_records)


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
