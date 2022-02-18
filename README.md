# NLPT_G3_A1

The project was carried out by Felix den Heijer, Elena Weber, and Jingyue Zhang during the seminar ‘NLP Technology' taught by Antske Fokkens and Pia Sommerauer at VU Amsterdam.

## Data

The folder [**data**](https://github.com/surferfelix/NLPT_G3_A1/tree/main/data) contains the mini data set in order to create the syntactic features. The mini data is a small extraction from the novel "Pride and Prejudice" by Jane Austen and was adapted from [**here**](https://www.gutenberg.org/files/1342/1342-h/1342-h.htm)

* `mini_data.tsv`

## Parsing

Before the feature extraction, three different parsers have been tried out: spaCy, NLTK with Stanford, and Stanza. In the end, it has been decided to use spaCy. The NLTK StanfordDependenyParser is being deprecated in the near future and thus does not contribute to further projects and since Stanza is running slower than spaCy it also has been decided against it.

## Embeddings
If you'd like to use pre-trained word embeddings (especially handy if size of input is small), then assign the path to the word embedding model to the `path_to_emb_model` variable. Note that the model should be txt not bin. the current implementation only supports 100 dimension embedding representations.

## Extracting Features

For the purpose of this project, we provide several functions in order to extract several syntactical and morphological features to use for NLP related tasks.

### Dependencies

Tokenises the data and extracts the dependency relation from each token. 
You can import the dependency extraction with,
* `from feature_extraction.py import get_dependencies`.
Once this is done you can provide the text you wish to extract dependencies for as a string, and the model will provide output as a tuple.
With the left item being the token, and the rightermost item being the dependency tag.
* `get_dependencies('This is a test for dependency extraction')`
Currently this implements the SpaCy dependency tags.

### Constituents

Tokenises the data and extracts constituents from each sentence.
You can import the constituency extraction with,
* `from feature_extraction.py import get_constituents`.
Once this is done you can provide the text you wish to extract constituents for as a string, and the model will provide output as a list.
The list contains a tuple-like output where the overarching items are in the outermost layer.

* Example: (S (NP (NP (DT The) (NN time)) (PP (IN for) (NP (NN action)))) (VP (VBZ is) (ADVP (RB now))) (. .))

### Head Extraction

Tokenises the data and extracts heads from each token.
You can import the head extraction with,
* `from feature_extraction.py import get_head`
Once this is done you can provide the text you wish to extract the head from as a string, and the model will provide output as a tuple.
With the left item being the token, and the rightermost item being the head of that token.

### Children Extraction

Tokenises the data and extracts children from each token.
You can import the children extraction with,
* `from feature_extraction.py import get_children`
Once this is done you can provide the text you wish to extract the children from as a string, and the model will provide output as a tuple.
With the left item being the token, and the rightermost item being all of the children of that token.

* Example: heard, [said, “, have, you, let, ?, ”]

### POS Tag Extraction

Tokenises the data and retrieves the POS tag representations of tokens. 
This can be imported into your project with 
* `from feature_extraction.py import get_pos`
Once this is done you can provide the text you wish to extract the POS tags from as a string, and the model will provide output as a list.

### Lemmatization

Tokenises the data and retrieves the lemmatized tokens. 
This can be imported into your project with 
* `from feature_extraction.py import get_lemma`
Once this is done you can provide the text you wish to extract the lemmas from as a string, and the model will provide output as a list.

### Previous Token Extraction

Tokenises the data and retrieves the previous token. If the previous index does not exist at an iteration, it will replace this with an empty string. 
This can be imported into your project with 
* `from feature_extraction.py import get_prev`
Once this is done you can provide the text you wish to extract the token from as a string, and the model will provide output as a list.

### Next Token Extraction

Tokenises the data and retrieves the next token. If the next index does not exist at an iteration, it will replace this with an empty string. 
This can be imported into your project with 
* `from feature_extraction.py import get_next`
Once this is done you can provide the text you wish to extract the token from as a string, and the model will provide output as a list.

This function can be imported with:
* `from feature_extraction.py import get_inflection_type`

### N-Gram Extraction

Tokenises the data and retrieves n-grams. This function takes two arguments, the input text which is to be tokenised, along with n, where n represents the window size. n = 2 will result in bi-grams etc. 
This can be imported into your project with 
* `from feature_extraction.py import get_word_ngrams`
Once this is done you can provide the text you wish to extract the token from as a string, and the model will provide output as a list.

### Customizing W2V to retrieve inflection type dictionary

This function will tokenise text and return a list of similar words to the target tokens in that text. 
Target tokens are selected based on the suffixes that you wish to look for in your text. You either look into a pre-trained embedding model, and if not defined then the model will try to use the input data to create a co-occurence matrix w2v style from there to compare to.

* **Selecting target tokens**

Target tokens are selected based on the *candidate_tokens* variable. You can provide a list of suffixes like so, and the model will look get all the words that end with those suffixes and return a list of similar embedding representations to those targets. 

* Example (and the default): `candidate_suffixes = ['s', 'ed', 'es', 'ing', 'e', 'eful']`

* **Selecting output type**

The `word_or_vector` argument can be either set to `"w"` or `"v"` to select whether you want a list of words, or a list of vectors as output. 

* **Loading your own Embedding Model**

This is generally recommended, especially if the inputdata is small. Load a KeyedVectors W2V embeddingsmodel and provide this as input to the `embeddingmodel` argument. Currently, this project only supports 100 dimensional embedding models. 

### Embedding Representation of Token Extraction

This function will extract an embedding representation of tokens and return a list of vectors. Note that currently, we only support 100 dimensional embedding models. You can import the function with

* `from feature_extraction.py import token_as_emb`

The embeddings can be extracted from the embeddingmodel argument. If this is not provided the model will attempt to use the inputs own co-occurences to create vectors. 

