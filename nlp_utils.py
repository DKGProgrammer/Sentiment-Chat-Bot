
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load models
nlp = spacy.load("en_core_web_sm")
vader = SentimentIntensityAnalyzer()

# Keyword-to-emotion mapping
KEYWORD_EMOTIONS = {
    "angry": ["angry", "furious", "annoyed", "mad", "irritated"],
    "fear": ["scared", "afraid", "terrified", "anxious", "nervous"],
    "disgust": ["disgusted", "gross", "revolted", "nasty"],
    "surprise": ["shocked", "surprised", "amazed", "startled"]
}

# Detect emotion using hybrid rules
def detect_emotion(text):
    doc = nlp(text.lower())
    vader_score = vader.polarity_scores(text)
    compound = vader_score["compound"]
    print(compound)

    # VADER-based base emotion
    if compound >= 0.5:
        base_emotion = "happy"
    elif compound <= -0.4767:
        base_emotion = "sad"
    else:
        base_emotion = "neutral"

    # Keyword override (more specific emotions)
    for token in doc:
        for emotion, keywords in KEYWORD_EMOTIONS.items():
            if token.lemma_ in keywords:
                return emotion  # override if detected

    return base_emotion
