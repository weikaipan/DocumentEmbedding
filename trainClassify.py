from toPickles import pickle_load
from sklearn.cluster import KMeans
from pprint import pprint
import pandas as pd
import numpy as np

def main():
	title2embeds = pickle_load("./title2embedding.p")
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
	kmeans = KMeans(n_clusters=1000, random_state=0).fit(X)
	news_data = pd.DataFrame(X)
	news_data['group'] = kmeans.labels_
	news_data['title'] = title_list


	print("Training Data Size = {}".format(news_data.shape))
	news_data.to_pickle('./news_embedding_2001_2005_group1000.p')

if __name__ == '__main__':
	main()