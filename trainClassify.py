from toPickles import pickle_load
from sklearn.cluster import KMeans


def main():
	title2embeds = pickle_load("./title2embedding.p")
	title2idx = {}
	idx2title = {}
	idx = 0
	X = []
	for title in title2embeds:
		title2idx[title] = 0
		idx2title[idx] = title
		X.append(title2embeds[title])

	kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
	print(kmeans.labels_)

if __name__ == '__main__':
	main()