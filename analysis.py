import pymongo
from textblob import TextBlob
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TwitterStreamData"]
collection = db["TwitterData"]

cursor = collection.find()
sentiment_scores = {}
for doc in cursor:
    for key, value in doc.items():
        if key != "_id":
            blob = TextBlob(value)
            sentiment_score = blob.sentiment.polarity
            sentiment_scores[key] = blob.sentiment.polarity

num_positive = sum(score > 0 for score in sentiment_scores.values())
num_negative = sum(score < 0 for score in sentiment_scores.values())
num_neutral = len(sentiment_scores) - num_positive - num_negative

def getPos():
    return num_positive
def getNeg():
    return num_negative
def getNeu():
    return num_neutral

