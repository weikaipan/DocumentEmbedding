import glob
from utility import clean_text, normalizeString
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
import pandas as pd
NEWS_PATH = '../data/news_csv/'

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
	all_news = glob.glob(NEWS_PATH+'*.csv')
	print(all_news)
	article = ""
	for news in all_news:
		df = pd.read_csv(news)
		print("Read file {}".format(news))
		for index, row in df.iterrows():
			cleaned_text = clean_text(normalizeString(row[5]))
			print(keep_noun_verb_adjs(row[5]))
			quit()
			article += keep_noun_verb_adjs(row[5])

	with open('../data/news/news_2001_2005.txt', 'w') as fout:
		fout.write(article)

if __name__ == '__main__':
	main()