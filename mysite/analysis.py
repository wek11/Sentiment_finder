"""
    Analysis file that gathers sentiment from a given link, given a text
"""

import nltk
import sorting
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Main analysis method, returns the sentiment with the correct one-word identifier
def gather_sentiment(text):
    stopwords = nltk.corpus.stopwords.words("english")
    total_score= 0.0

    avg = 0.0
    words = nltk.word_tokenize(text)

    sentences = text.split("|")
    words = [w for w in words if w.isalpha()]
    if len(sentences) == 0:
        return "N/A"
    freq = nltk.FreqDist(words)

    for sentence in sentences:
        total_score += sia.polarity_scores(sentence)["compound"]


    total_score /= len(sentences)
    out_str = "Score: " + str(round(total_score, 3))
    if (total_score < -0.5):
        return (out_str + ". This page is very negative "), "very_negative"
    elif (total_score < -.1): 
        return (out_str + ". This page is negative "), "negative"
    elif (total_score < .1):
        return (out_str + ". This page is neutral "), "neutral"
    elif (total_score < .5):
        return (out_str + ". This page is postive "), "positive"
    elif (total_score < 1):
        return (out_str + ". This page is very positive "), "very_positive"