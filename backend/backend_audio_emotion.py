import librosa
import numpy as np

def analyze_emotion(audio_path):
    y, sr = librosa.load(audio_path, sr=22050)
    pitch = np.mean(librosa.yin(y, fmin=50, fmax=300))
    energy = np.mean(librosa.feature.rms(y=y))

    if pitch > 200 and energy < 0.1:  # High pitch, low energy → Fear
        return "fear"
    return "normal"

def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path, sr=22050)

    # Extract Pitch (Fundamental Frequency)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Extract Zero-Crossing Rate (Indicates sharpness/agitation)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))

    # Extract Spectral Centroid (Bright/Loud Speech Detection)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    # Extract RMS Energy (Loudness)
    rms_energy = np.mean(librosa.feature.rms(y=y))

    # Extract Mel-Frequency Cepstral Coefficients (MFCCs)
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)

    return {
        "pitch": float(np.mean(pitches[pitches > 0])),  
        "zcr": float(zcr),
        "spectral_centroid": float(spectral_centroid),
        "rms_energy": float(rms_energy),
        "mfccs": [float(x) for x in mfccs]  # Convert MFCCs list to Python floats
    }


if __name__ == "__main__":
    audio_path = r"data\Recording (2).wav"
    emotion = analyze_emotion(audio_path)
    audio_features = extract_audio_features(audio_path)
    print(f"Emotion: {emotion}")
    print(f"Audio Features: {audio_features}")