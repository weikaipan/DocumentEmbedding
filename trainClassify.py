from toPickles import pickle_load
from sklearn.cluster import KMeans
from pprint import pprint
import pandas as pd
import numpy as np
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-k", "--clusters", required=True,
	help="Number of clusters you specify")
ap.add_argument("-f", "--title2embedding", required=False,
	help="Article Embedding {title: [embds, ...]}")
args = vars(ap.parse_args())

def main():
	# args
	print("Configurations...")
	for k in args:
		print("{}: {}".format(k, args[k]))
	TITLE2EMBEDS = "./title2embedding.p"
	if "title2embedding" in args:
		TITLE2EMBEDS = args["title2embedding"]
	# loads
	title2embeds = pickle_load(TITLE2EMBEDS)
	# main starts
	title2idx = {}
	idx2title = {}
	idx = 0
	X = []
	title_list = []
	for title in title2embeds:
		title2idx[title] = 0
		idx2title[idx] = title
		title_list.append(title)
		X.append(title2embeds[title].tolist())
	kmeans = KMeans(n_clusters=args["clusters"], random_state=0).fit(X)
	news_data = pd.DataFrame(X)
	news_data['group'] = kmeans.labels_
	news_data['title'] = title_list

	print("Training Data Size = {}".format(news_data.shape))
	news_data.to_pickle('./news_embedding_2001_2005_group1000.p')

if __name__ == '__main__':
	main()