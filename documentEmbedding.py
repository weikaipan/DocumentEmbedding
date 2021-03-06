"""This file embeds news articles using fasttext"""
from pprint import pprint
from toPickles import pickle_load, pickle_dump
from nltk import word_tokenize
import numpy as np
import os.path
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--title2news", required=False, 
	help="A pickle file containing the dictionary with article title to their text")
ap.add_argument("-o", "--output", required=False,
	help="Optional output destination, default as ./title2embedding.p")
args = vars(ap.parse_args())

def article_embedding(document, word2vec):
	"""Concat the max and min vector"""
	DIM = len(word2vec['the'])
	tokens = word_tokenize(document.lower())    
	embedding_max = np.array([-999.0]*DIM)
	embedding_min = np.array([999.0]*DIM)
	for word in tokens:
		try:
			word_vector = np.array([float(i) for i in word2vec[word]])
			embedding_max = np.maximum(embedding_max, word_vector)
			embedding_min = np.minimum(embedding_min, word_vector)
		except KeyError:
			pass
	embedding = np.append(embedding_max, embedding_min)
	embedding = embedding / np.linalg.norm(embedding)
	return embedding

def parse_word2vec(word2vec):
	w2v = {}
	for wordvec in word2vec:
		w2v[wordvec[0]] = wordvec[1:-1]
	return w2v

def main():
	"""
	Reads in the model.vec generated by the fasttext
	"""
	print("Configurations...")
	for k in args:
		print("{}: {}".format(k, args[k]))

	if os.path.isfile("./word2vec.p"):
		print("Loading word2vec pickle...")
		word2vec = pickle_load("./word2vec.p")
	else:
		print("Writing word2vec pickle...")
		word2vec = []
		with open("./model.vec") as f:
			next(f)
			for line in f:
				"""
				Looks like:
					['vocab', ...., '\n']
				"""
				word2vec.append(line.split(" "))
		word2vec = parse_word2vec(word2vec)
		pickle_dump(word2vec, "./word2vec.p")

	"""
	title2news:
		a dicitonary {title: news text, ...}
	"""
	TITLENEWS_PATH = "./title2news.p"
	if "title2news" in args:
		TITLENEWS_PATH = args["title2news"]
	title2news = pickle_load(TITLENEWS_PATH)
	print("Load title2news")
	"""
	create the 
		a dictionary {title1: [v1, v2, ...], title2: [...]}
	"""
	doc2embedding = {}
	i = 0
	print("Total News = {}".format(len(title2news)))
	print("Begin vectorize articles")
	for title, news in title2news.items():
		i = i + 1
		if i % 100 == 0:
			print("Processing on article: ", i)
		doc2embedding[title] = article_embedding(news, word2vec)
	"""
	save the file
	"""
	OUTPUT_PATH = './'
	if "output" in args:
		OUTPUT_PATH = args["output"]
	pickle_dump(doc2embedding, OUTPUT_PATH+'title2embedding.p')

if __name__ == '__main__':
	main()