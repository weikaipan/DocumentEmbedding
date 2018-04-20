# DocumentEmbedding

## Decription:

**DocumentEmbedding embeds articles using word vectors trained by language model and applies vector operations to produce a vector representation of an aritcle. The language model applies ```fasttext```. For more use in fasttext, please refer to this [link](https://github.com/facebookresearch/fastText).**

## Usage:

### 1. Preprocess articles as textfile

#### Input
A series of text files.
#### Output
``data.txt`` which contains all concatenation of input text files.

In this step, concatenating all article text into one ```data.txt``` file.


### 2. Apply ``fasttext`` to train the vocabulary set using language model

#### Input
```data.txt``` which is from above output.
#### Output
```model.bin```, ```model.vec```

**(For configurations of ``fasttext``, please refer to the [link](https://github.com/facebookresearch/fastText).)**

After the text file is ready, type below command, which uses ```skipgram``` (or ```cbow```by option)  to train word representation using language model.

```$ ./fasttext skipgram -input data.txt -output model```

Above command generates ```model.bin``` and ```model.vec```, where ```model.vec``` includes all vocabularies in the ```data.txt```, with their vector representation.

Please see the snapshot below of the ```model.vec```:

```
61428 100

the -0.33771 0.08457 -0.1696 ...
to -0.23626 -0.069627 -0.41499 ...
...
```
where ```data.txt``` has ```61428``` vocabularies, and each word has ```100``` dimensions of its word representation.

Note that the values of each dimension has no actually meanings, they are just the position in the vector space.



### 3. Concate Word Representation into Article Representation

#### Input
```title2article.p``` which is a python dictionary that has the structure of ```{title: text}```.

```word2vec.p``` or ```model.vec```, where ```word2vec.p``` is the preprocessed word vectors, and ```model.vec``` is the vanilla output of fasttext.

#### Output
```[output dir]/title2embedding.p```, is a python dictionary containing ```{title: [%f, %f, ...]}```


```$ python documentEmbedding.py -t [load pickle of title2news] -o [the output directory]```

This python script searches the current director, if the pickle file of preprocessed word vectors does not exist, it 
1. **Reads in the ```model.vec```**
2. **Preprocess vectors in ```model.vec```**
3. **Maps aritcle title to the article representation**




#### In the function ```article_embedding```:

it takes ```document``` and ```word2vec```.

The parameter: ```document``` is the plain text in the ```title2news.p``` for each text mapped to its title.

The parameter ```word2vec``` is the preprocessed vector represenation of each word.

**This function does the following:**

1. Find the dimension of word representation.
2. Tokenize the article using ``nltk.work_tokenize``
3. Find dimension-wise maximum and minimum values, then concatenate both vector.
4. The result will be a 200 dimensional vector representation.

Note: above approach to represent an ariticle is just an experiement without founded theories.


### 4. Cluster Articles using Kmeans Clustering

#### Input
```./title2embedding.p``` or the output from **step 3**.
#### Output
```./news_embedding_2001_2005_group[k].p```
which contains a dictionary with:
```
{
	'group1': [title1, title2, ...]
	.. k groups in total
}
```

Simply type and give the following option: 
```python trainClassify.py -k [clusters] -f [input pickle file path]```
which will cluster news data by group of **clusters**.

This script applies kmeans clustering in sklearn to cluster article vectors into [clusters] groups.

### Note

1. toNews.py

```$ python toNews.py -n [path to all article csv] -k [specify if you only want noun and adjs]```

Takes news files in csv and cleaned the text.