import benepar, spacy
import csv

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

def main(data):
    #Pipeline goes in here
    to_extract = read_data(data)
    tokens, dependencies = get_dependencies(to_extract)
    consts = get_constituents(to_extract)
    print(consts)

if __name__ == '__main__':
    data = 'data/mini_data.tsv' # String to filepath in here
    main(data)