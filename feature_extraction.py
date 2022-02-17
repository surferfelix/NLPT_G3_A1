import benepar, spacy
import csv
from spacy import displacy
import gensim
from gensim.models import Word2Vec
import nltk
from nltk.stem import WordNetLemmatizer
import pandas as pd
from gensim.models import KeyedVectors
import os

def read_data(path: str) -> list:
    '''reads the data to use for feature_extraction
    :param: data: string with path to tsv file'''
    container = list()
    with open(path) as file:
        # uncomment when using a csv file:
        # infile = csv.reader(file, delimiter = '\t')
        for i in file:
            container.append(i)
    return container

def initialise_spacy():
    '''Loads a vocabulary to use'''
    nlp = spacy.load('en_core_web_lg')
    return nlp

def get_dependencies(input: list) -> list:
    '''Will retrieve dependencies for each text part in list'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    tokens = [token.text for token in doc]
    dependencies = [token.dep_ for token in doc]
    return tokens, dependencies

def vis_dependencies(input: list) -> list:
    '''Visualize the dependency relation
    :param doc: takes as input the dependencies to be visualized'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    sentence_spans = list(doc.sents)
    displacy.serve(sentence_spans, style="dep")
    
def get_constituents(input: list) -> list: 
    '''Will retrieve constituents for each text part in list'''
    #inspired by [https://github.com/nikitakit/self-attentive-parser][16-02-2022]
    nlp = initialise_spacy()
    nlp.add_pipe('benepar', config = {'model':'benepar_en3'})
    container = []
    doc = nlp(input[0])
    for sent in list(doc.sents):
        container.append(sent._.parse_string)
    return container

    #other tried approach taken from [https://stackoverflow.com/questions/56896753/is-there-a-way-to-get-entire-constituents-using-spacy] [16-02-2022]  
    # for token in nlp(input[0]): # Make input[0] into for loop
    #     if token.pos_ in ['NOUN', 'ADJ']:
    #         if token.dep_ in ['attr', 'acomp'] and token.head.lemma_ == 'be':
    #             print([t.text for t in token.subtree])

def get_head(input: list) -> tuple:
    '''This function will return the head word in the sentence or subclause that is being iterated over
    :return: tuple of two lists'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    span = doc[doc[4].left_edge.i : doc[4].right_edge.i+1]
    container = []
    tokens = []
    with doc.retokenize() as retokenizer:
        retokenizer.merge(span)
    for token in doc:
        tokens.append(tokens)
        container.append(token.head.text)
    return tokens, container

def get_children(input: list) -> tuple:
    '''Will return all children of target word
    :return: tuple of two lists'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    children = []
    tokens = []
    for token in doc:
        tokens.append(token.text)
        children.append(token.children)
    return tokens, children

def get_lemma(input: str) -> list:
    '''Will return a list of lemmas'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    lemma = []
    for token in doc:
        lemma.append(token.lemma_)
    return lemma

def get_pos(input: str) -> list:
    '''Will return a list of POS tags'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    pos_tags = []
    for token in doc:
        pos_tags.append(token.pos_)
    return pos_tags

def get_prev(input: str) -> list:
    '''Will return a list of previous token'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    tokens = [token for token in doc]
    prev_tokens = []
    for index, token in enumerate(tokens):
        try: 
            prev = tokens[index-1]
        except IndexError:
            prev = ''
        prev_tokens.append(prev)
    return prev_tokens

def get_next(input: str) -> list:
    '''Will return a list of next token'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    tokens = [token for token in doc]
    next_tokens = []
    for index, token in enumerate(tokens):
        try: 
            next = tokens[index+1]
        except IndexError:
            next = ''
        next_tokens.append(next)
    return next_tokens

def get_inflection_type(input, embeddingmodel = False) -> list:
    '''Morphology classification using w2v. Will return a list of regular inflections
    :param embeddingmodel:, a gensim loaded w2v style embedding model. If you wish to use the inputs own
    vocabulary to train a model, you can leave this empty
    :type embeddingmodel: gensim w2v object or falsey object if not including model'''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    # Inspired by DOI:10.3115/1117601.1117615 to figure this out
    # 1. Selecting candidate affixes
    candidate_suffixes = ['s', 'ed', 'es', 'ing', 'e', 'eful']
    # 2. Getting co-occurence matrix for words with these affixes
    tokens = [token.text for token in doc]
    if not embeddingmodel:
        language_model = Word2Vec(tokens, min_count=200) # Change min_count for smaller datasets (needs to be proportional)
        language_model = language_model.wv
    elif embeddingmodel:
        language_model = embeddingmodel
    # 2.1 Selecting the words from W2V with the candidate suffixes to get their vector reps
    container = []
    for tok in tokens:
        for suffix in candidate_suffixes:
            if tok.endswith(suffix):
                #print(tok)
                if tok in language_model:
                    rep = language_model[tok]
                else: 
                    rep = [0] * 100
                container.append(rep)
    # 3. Getting the words with similar semantic vectors
    regular_infl = []
    for vector in container:
        for word in language_model.most_similar(vector):
            w,v = word
            for suf in candidate_suffixes:
                if w.endswith(suf):
                    regular_infl.append(w)
    print(regular_infl)
    return regular_infl

def get_word_ngrams(input: str) -> list:
    '''
    This function generates n word ngrams
    :return: all possible ngrams
    '''
    nlp = initialise_spacy()
    doc = nlp(input[0])
    tokens = [token for token in doc]

    word_grams= pd.Series(nltk.ngrams(tokens, pad_right = True))
    
    return word_grams

def main(data, path_to_emb = ''):
    # Loading embeddings 
    if path_to_emb:
        word_vectors = KeyedVectors.load_word2vec_format(path_to_emb)
    #Pipeline goes in here
    to_extract = read_data(data)
    tokens, dependencies = get_dependencies(to_extract)
    consts = get_constituents(to_extract)
    tokens, heads = get_head(to_extract)
    tokens, children = get_children(to_extract)
    lemma = get_lemma(to_extract)
    pos_tags = get_pos(to_extract)
    prev_token = get_prev(to_extract)
    next_token = get_next(to_extract)
    # word_n_grams = get_word_ngrams(to_extract)
    regular_infl_words = get_inflection_type(to_extract, word_vectors)
    #print(regular_infl_words)

if __name__ == '__main__':
    data = 'data/mini_data.tsv' # String to filepath in here
    path_to_emb_model = ''
    main(data, path_to_emb_model)