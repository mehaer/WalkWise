from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from backend_audio import transcribe_audio

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment

if __name__ == "__main__":
    audio_path = r"data\Recording (3).wav"
    transcript = transcribe_audio(audio_path)
    sentiment = analyze_sentiment(transcript)
    print(f"Sentiment: {sentiment}")
