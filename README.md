# NLPT_G3_A1

The project was carried out by Felix den Heijer, Elena Weber, and Jingyue Zhang during the seminar ‘NLP Technology' taught by Antske Fokkens and Pia Sommerauer at VU Amsterdam.

## Data

The folder [**data**](https://github.com/surferfelix/NLPT_G3_A1/tree/main/data) contains the mini data set in order to create the syntactic features. The mini data is a small extraction from the novel "Pride and Prejudice" by Jane Austen and was adapted from [**here**](https://www.gutenberg.org/files/1342/1342-h/1342-h.htm)

* `mini_data.tsv`

## Parsing

Before the feature extraction, three different parsers have been tried out: spaCy, NLTK with Stanford, and Stanza. In the end, it has been decided to use spaCy. The NLTK StanfordDependenyParser is being deprecated in the near future and thus does not contribute to further projects and since Stanza is running slower than spaCy it also has been decided against it.

## Embeddings
If you'd like to use pre-trained word embeddings (especially handy if size of input is small), then assign the path to the word embedding model to the 
`path_to_emb_model` variable. 


## Extracting Features

For the purpose of this project, we provide several functions in order to extract several syntactical and morphological features to use for NLP related tasks.

### Dependencies

You can import the dependency extraction with,
`from feature_extraction.py import get_dependencies`.
Once this is done you can provide the text you wish to extract dependencies for as a string, and the model will provide output as a tuple.
With the left item being the token, and the rightermost item being the dependency tag.
`get_dependencies('This is a test for dependency extraction')`
Currently this implements the SpaCy dependency tags.

### Constituents

You can import the constituency extraction with,
`from feature_extraction.py import get_constituents`.
Once this is done you can provide the text you wish to extract constituents for as a string, and the model will provide output as a list.
The list contains a tuple-like output where the overarching items are in the outermost layer.

* Example: (S (NP (NP (DT The) (NN time)) (PP (IN for) (NP (NN action)))) (VP (VBZ is) (ADVP (RB now))) (. .))

### Head Extraction

You can import the head extraction with,
`from feature_extraction.py import get_head`
Once this is done you can provide the text you wish to extract the head from as a string, and the model will provide output as a tuple.
With the left item being the token, and the rightermost item being the head of that token.

### Children Extraction

You can import the children extraction with,
`from feature_extraction.py import get_children`
Once this is done you can provide the text you wish to extract the children from as a string, and the model will provide output as a tuple.
With the left item being the token, and the rightermost item being all of the children of that token.

* Example: heard, [said, “, have, you, let, ?, ”]