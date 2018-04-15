import pandas as pd
import unicodedata
import string
import re
import pickle
import glob
import json

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def remove_non_ascii(text):
	"""
	Note:
	 ord('a') returns the integer 97 , ord(u'\u2020') returns 8224 .
	"""
	return ''.join([i if ord(i) < 128 else ' ' for i in text])

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = remove_non_ascii(s)
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?']+", r" ", s)
    return str(s.encode('utf-8').decode('ascii', 'ignore'))

def clean_text(text):
	return text.replace("lead:", "")

def json_load(file_path):
	with open(file_path, "r") as f:
		return json.load(f)


def pickle_dump(obj, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

def pickle_load(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

def read_news(NEWS_PATH):
	all_news = glob.glob(NEWS_PATH+'*.csv')
	article = {}
	for news in all_news:
		df = pd.read_csv(news)
		print("Read file {}".format(news))
		for index, row in df.iterrows():
			title = row[4].replace("'", "")
			cleaned_text = clean_text(normalizeString(row[5]))
			article[title] = cleaned_text
	pickle_dump(article, './title2news.p')

if __name__ == '__main__':
	read_news('./news_csv/')

