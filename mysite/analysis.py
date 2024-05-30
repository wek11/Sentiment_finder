import nltk
import sorting
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

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
        #print(sia.polarity_scores(sentence)["compound"])
        #print(">", is_positive(sentence), sentence)
        total_score += sia.polarity_scores(sentence)["compound"]


    total_score /= len(sentences)

    if (total_score < -0.5):
        return ['very negative', total_score]
    elif (total_score < -.1): 
        return ['negative', total_score]
    elif (total_score < .1):
        return ['neutral', total_score]
    elif (total_score < .5):
        return ['positive', total_score]
    elif (total_score < 1):
        return ['very positive', total_score]

def is_positive(sentence: str) -> bool:
    return sia.polarity_scores(sentence)["compound"] > 0