import benepar, spacy
import csv
from spacy import displacy


def read_data(path: str) -> list:
    '''reads the data to use for feature_extraction
    :param: data: string with path to tsv file'''
    container = list()
    with open(path) as file:
        infile = csv.reader(file, delimiter = '\t')
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

def main(data):
    #Pipeline goes in here
    to_extract = read_data(data)
    tokens, dependencies = get_dependencies(to_extract)
    consts = get_constituents(to_extract)
    tokens, heads = get_head(to_extract)
    get_children(to_extract)
if __name__ == '__main__':
    data = 'data/mini_data.tsv' # String to filepath in here
    main(data)