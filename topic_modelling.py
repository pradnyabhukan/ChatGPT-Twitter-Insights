import pymongo
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TwitterStreamData"]
collection = db["TwitterData"]

# Retrieve data from collection
data = collection.find({}, {"_id": 1, "text": 1}) # Retrieve "_id" and "text" fields

# Create DataFrame from MongoDB data
df = pd.DataFrame(list(data))

# Define preprocessing functions
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove mentions and hashtags
    text = re.sub(r'@[^\s]+', '', text)
    text = re.sub(r'#', '', text)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    
    # Tokenize text into words
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Join words back into text
    text = ' '.join(words)
    
    return text

# Apply preprocessing function to '_id' field and create 'preprocessed_text' column
df['preprocessed_text'] = df['_id']
df['preprocessed_text'] = df['preprocessed_text'].apply(preprocess_text)

# Store updated DataFrame in MongoDB collection
for _, row in df.iterrows():
    collection.update_one({'_id': row['_id']}, {'$set': {'preprocessed_text': row['preprocessed_text']}})
