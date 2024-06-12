import pymongo
import networkx as nx

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

# calculate the metrics for each node
degree_centrality = nx.degree_centrality(G)
in_degree_centrality = G.in_degree()
out_degree_centrality = G.out_degree()
betweenness_centrality = nx.betweenness_centrality(G)
# eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-6, weight='weight')

# print the metrics for the top 10 nodes with the highest degree centrality
top_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by degree centrality:")
for node, centrality in top_degree_centrality:
    print(f"{node}: {centrality:.3f}")

# print the metrics for the top 10 nodes with the highest in-degree centrality
top_in_degree_centrality = sorted(in_degree_centrality, key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by in-degree centrality:")
for node, centrality in top_in_degree_centrality:
    print(f"{node}: {centrality}")

# print the metrics for the top 10 nodes with the highest out-degree centrality
top_out_degree_centrality = sorted(out_degree_centrality, key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by out-degree centrality:")
for node, centrality in top_out_degree_centrality:
    print(f"{node}: {centrality}")

# print the metrics for the top 10 nodes with the highest betweenness centrality
top_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)
