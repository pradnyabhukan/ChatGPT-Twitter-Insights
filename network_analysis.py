import pymongo
import networkx as nx
import matplotlib.pyplot as plt

# create a MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")

# select the database and collection you want to work with
db = client["TwitterStreamData"]
collection = db["TwitterData1"]

# create a dictionary to store the counts of each location
location_counts = {}

# query the collection to retrieve all documents
documents = collection.find()

# create a directed graph to represent the retweet relationships
G = nx.DiGraph()

# loop over the documents and count the number of documents from each location
for doc in documents:
    id = doc["_id"]
    doc_with_id = collection.find_one({"_id": id})
    doc = list(doc_with_id.values())[-1]
    retweets = doc[1]
    likes = doc[2]
    location = doc[3]

    # update the count of documents from this location
    if location in location_counts:
        location_counts[location] += 1
    else:
        location_counts[location] = 1

    # add an edge to the graph for each retweet
    if retweets > 0:
        G.add_edge(doc[0], doc[1], weight=retweets)

nx.write_gexf(G, "retweet_network.gexf")
# Draw the graph
nx.draw(G, with_labels=True)

# Show the graph
plt.show()