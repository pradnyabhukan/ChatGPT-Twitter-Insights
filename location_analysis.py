import pymongo

# create a MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")

# select the database and collection you want to work with
db = client["TwitterStreamData"]
collection = db["TwitterData1"]

location_counts = {}

documents = collection.find()



for doc in documents:
    id = doc["_id"]
    doc_with_id = collection.find_one({"_id": id})
    doc = list(doc_with_id.values())[-1]
    location = doc[3]
    ##print(location)
    if location:
        if location in location_counts:
            location_counts[location] += 1
        else:
            location_counts[location] = 1

sorted_counts = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)

locations = []
counts = []

for location, count in sorted_counts[:10]:
    locations.append(location)
    counts.append(count)

def getLoc():
    ##print(locations)
    return locations
def getCount():
    print(counts)
    return counts

