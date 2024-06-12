import pymongo
import re
import pandas as pd


# create an empty list to store hashtags
hashtags = []

# establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TwitterStreamData"]
collection = db["TwitterData"]


cursor = collection.find()
for doc in cursor:
    for key, value in doc.items():
        if key != "_id":
            text = value
            # find all hashtags in the tweet using regular expression
            hashtags_in_tweet = re.findall(r'#\w+', text)
            # add the hashtags to the list
            hashtags.extend(hashtags_in_tweet)

# create a Pandas DataFrame to store the hashtags and their frequency
df_hashtags = pd.DataFrame(hashtags, columns=['hashtag'])
df_hashtags['frequency'] = df_hashtags.groupby('hashtag')['hashtag'].transform('count')
df_hashtags = df_hashtags.drop_duplicates().reset_index(drop=True)
df_hashtags = df_hashtags.sort_values('frequency', ascending=False)

# print the top 20 hashtags and their frequency
def getHashTags():
    return df_hashtags.head(20)
