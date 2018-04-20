import glob
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import argparse
NEWS_PATH = '../data/news_csv/'

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--NEWS_PATH", required=False, help="Given article directory")
ap.add_argument("-k", "--KEEP", required=False, help="Only keep noun, adj, verbs")
args = vars(ap.parse_args())

def keep_noun_verb_adjs(text):
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(text.lower())
	return " ".join(tokens)

def main():
	"""
	Protocol:
	output:
	{ 'title': {
			'utime': time
			'geo': loc
			'content': body
		}
	}
	"""
	print("Configurations...")
	for k in args:
		print("{}: {}".format(k, args[k]))
	if "NEWS_PATH" in args:
		NEWS_PATH = args["NEWS_PATH"]
	all_news = glob.glob(NEWS_PATH+'*.csv')
	print(all_news)

	
	article = ""
	for news in all_news:
		df = pd.read_csv(news)
		print("Read file {}".format(news))
		for index, row in df.iterrows():
			if "KEEP" in args:
				cleaned_text = keep_noun_verb_adjs(clean_text(normalizeString(row[5])))
			else:
				cleaned_text = clean_text(normalizeString(row[5]))
			

	with open(NEWS_PATH+'news_2001_2005.txt', 'w') as fout:
		fout.write(article)

if __name__ == '__main__':
	main()