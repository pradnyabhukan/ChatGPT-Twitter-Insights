import pymongo

# create a MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")

# select the database and collection you want to work with
db = client["TwitterStreamData"]
collection = db["TwitterData1"]

# create a dictionary to store the counts of each location
location_counts = {}

# query the collection to retrieve all documents
documents = collection.find()

# loop over the documents and count the number of documents from each location
for doc in documents:
    id = doc["_id"]
    doc_with_id = collection.find_one({"_id": id})
    doc = list(doc_with_id.values())[-1]
    retweets = doc[1]
    likes = doc[2]
    location = doc[3]
    
