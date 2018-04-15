"""This file embeds news articles using fasttext"""
from pprint import pprint
from toPickles import pickle_load, pickle_dump
from nltk import word_tokenize
import numpy as np
import os.path


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
	title2news = pickle_load("./title2news.p")
	doc2embedding = {}
	for title, news in title2news.items():
		doc2embedding[title] = article_embedding(news, word2vec)
	pprint(doc2embedding)
	pickle_dump(doc2embedding, "./title2embedding.p")
	# save the file

if __name__ == '__main__':
	main()