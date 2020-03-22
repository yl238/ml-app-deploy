import argparse
import spacy, en_core_web_md
from nltk import 

nlp = en_core_web_md.load()


def parse_arguments():
    """
    Return: str
        The text to be edited
    """
    parser = argparse.ArgumentParser(
        description="Receive text to be edited"
    )
    parser.add_argument(
        'text',
        metavar='input text',
        type=str
    )
    args = parser.parse_args()
    return args.text


def clean_input(text):
    """Sanitize text, without non-ascii characters
    
    Parameters
    ----------
    text : str
        User input text
    """
    return str(text.encode().decode('ascii', errors='ignore'))


def preprocess_input(text):
    """Return text ready to be fed into analysis, by having 
    sentences and words tokenized
    
    Parameters
    ----------
    text : str
        Sanitized text
    """
    doc = nlp(text)
    tokens = [[token.text for token in sent] for sent in doc.sents]
    return tokens


def count_word_usage(tokens, words):
    """Count the number of appearance of the words 
    in the list of tokens
    
    Parameters
    ----------
    tokens : list
        Tokens
    words : list
        The words which we want to count number of appearance
    """
    counts = 0
    for word in words:
        counts +=  tokens.count(word)
    return counts
    


def get_suggestions(text):
    """Returns a string containing our suggestions
    
    Parameters
    ----------
    sentence_list : str
        a list of sentences, each being a list of words
    """
    doc = nlp(text)

    told_said_usage = sum(count_word_usage(tokens.text, ['told', 'said']) for tokens in doc)
    but_and_usage = sum(count_word_usage(tokens.text, ['but', 'and']) for tokens in doc)
    wh_adverbs_usage = sum(count_word_usage(
        tokens.text,
        [
            "when",
            "where",
            "why",
            "whence",
            "whereby",
            "wherein",
            "whereupon"
        ]) 
        for tokens in doc)
    result_str = ""
    adverb_usage = "Adverb usage: {} told/said, {} but/and, {} wh-adverbs".format(
        told_said_usage,
        but_and_usage,
        wh_adverbs_usage
    )
    result_str += adverb_usage
    tokens = [token.text for token in doc if token.is_punct != True]
    

        