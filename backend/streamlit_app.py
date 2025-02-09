import streamlit as st
import requests
import io

# Flask API Base URL
FLASK_API_URL = "http://127.0.0.1:5000"

# Page title
st.title("Emergency Audio Detection System")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Upload & Process", "Analyze Sentiment", "View Metadata"])

# --- Upload & Process Audio ---
if menu == "Upload & Process":
    st.header("📤 Upload Audio for Processing")

    # Use session state to prevent reload issues
    if "uploaded_audio" not in st.session_state:
        st.session_state["uploaded_audio"] = None

    uploaded_file = st.file_uploader("Upload an audio file (wav/m4a/mp3)", type=["wav", "m4a", "mp3"])

    if uploaded_file:
        st.session_state["uploaded_audio"] = uploaded_file  # Store uploaded file in session state

    if st.session_state["uploaded_audio"]:
        st.audio(st.session_state["uploaded_audio"], format="audio/wav")
        filename = st.session_state["uploaded_audio"].name

        # Send file to Flask API
        if st.button("Process Audio"):
            files = {"audio": (filename, st.session_state["uploaded_audio"], "audio/wav")}
            response = requests.post(f"{FLASK_API_URL}/process", files=files)

            if response.status_code == 200:
                data = response.json()
                st.success("Audio Processed Successfully!")
                st.write("**Transcript:**", data["transcript"])
                st.write("**Emergency Detected:**", data["emergency_detected"])
                st.write("**Message:**", data["message"])
            else:
                st.error("Error processing audio.")

# --- Analyze Sentiment ---
elif menu == "Analyze Sentiment":
    st.header("🎭 Sentiment Analysis (Fear Detection)")

    if "sentiment_audio" not in st.session_state:
        st.session_state["sentiment_audio"] = None

    uploaded_file = st.file_uploader("Upload an audio file for sentiment analysis", type=["wav", "m4a", "mp3"])

    if uploaded_file:
        st.session_state["sentiment_audio"] = uploaded_file

    if st.session_state["sentiment_audio"]:
        st.audio(st.session_state["sentiment_audio"], format="audio/wav")
        filename = st.session_state["sentiment_audio"].name

        # Send file to Flask API
        if st.button("Analyze Emotion"):
            files = {"audio": (filename, st.session_state["sentiment_audio"], "audio/wav")}
            response = requests.post(f"{FLASK_API_URL}/sentiment", files=files)

            if response.status_code == 200:
                data = response.json()
                st.success("Sentiment Analysis Completed!")
                st.write("**Detected Emotion:**", data["emotion"])
                st.write("**Emergency Detected:**", data["emergency_detected"])
                st.write("**Audio Features:**", data["audio_features"])
                st.write("**Message:**", data["message"])
            else:
                st.error("Error analyzing emotion.")

# --- View Metadata ---
elif menu == "View Metadata":
    st.header("View Stored Audio Metadata")

    if st.button("Fetch Metadata"):
        response = requests.get(f"{FLASK_API_URL}/audio_metadata")

        if response.status_code == 200:
            metadata = response.json()
            if metadata:
                for item in metadata:
                    st.write(f"**File**: {item['filename']}")
                    st.write(f"**Emotion**: {item.get('emotion', 'N/A')}")
                    st.write(f"**Emergency Detected**: {item['emergency_detected']}")
                    st.write("---")
            else:
                st.warning("No audio metadata found.")
        else:
            st.error("Error retrieving metadata.")
