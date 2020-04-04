import argparse
import syllables
import spacy, en_core_web_md

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

    tokens = [token.text for token in doc if token.is_alpha == True]
    print(tokens)

    told_said_usage = count_word_usage(tokens, ['told', 'said'])
    but_and_usage = count_word_usage(tokens, ['but', 'and'])
    wh_adverbs_usage = count_word_usage(
        tokens,
        [
            "when",
            "where",
            "why",
            "whence",
            "whereby",
            "wherein",
            "whereupon"
        ])

    result_str = ""
    adverb_usage = "Adverb usage: {} told/said, {} but/and, {} wh-adverbs".format(
        told_said_usage,
        but_and_usage,
        wh_adverbs_usage
    )
    result_str += adverb_usage
    
    
    average_word_length = sum([len(token) for token in tokens]) / len(tokens)
    unique_words_fraction = len(set(tokens)) / len(tokens)

    word_stats = "Average word length {:2f}, fraction of unique words {:.2f}".format(
        average_word_length, unique_words_fraction)

    # Using HTML break to later display on a webapp
    result_str += '\n'
    result_str += word_stats

    number_of_syllables = count_total_syllables(tokens)
    number_of_words = len(tokens)
    number_of_sentences = len([sent for sent in doc.sents])

    syllable_counts = "{:d} syllables, {:d} words, {:d} sentences".format(
        number_of_syllables,
        number_of_words,
        number_of_sentences
    )
    result_str += '\n'
    result_str += syllable_counts

    flesch_score = compute_flesch_reading_ease(
        number_of_syllables, number_of_words, number_of_sentences
    )

    flesch = "{:d} syllables, {:.2f} flesch score: {}".format(
        number_of_syllables,
        flesch_score,
        get_reading_level_from_flesch(flesch_score)
    ) 
    result_str += "\n"
    result_str += flesch


    return result_str

def count_total_syllables(tokens):
    """Count the total number of syllables using the 
    package `syllables`
    
    Parameters
    ----------
    tokens : list of str
        Words to count syllables
    
    Returns
    -------
    int
        Total number of syllables in list
    """
    return syllables.estimate(' '.join(tokens))


def compute_flesch_reading_ease(n_syllables, n_words, n_sents):
    """Compute Flesch Reading ease
    
    Parameters
    ----------
    n_syllables : int
        Number of syllables in text
    n_words : int
        Number of words in text
    n_sents : int
        Number of sentences in text
    
    Returns
    -------
    float
        flesch-kincaid reading ease
    """
    avg_sent_length = n_words / n_sents
    avg_word_length_in_syllables = n_syllables / n_words

    return 206.835 - (1.015 * avg_sent_length) - (84.6 * avg_word_length_in_syllables) 

def get_reading_level_from_flesch(fs):
    """Calculate reading level from the Flesch-Kincaid score.
    Here we calculate it from the syllable, words and sentence count
    but it can be considered as the inverse of the Flesch score.
    
    Parameters
    ----------
    fs: float
        Flesch score used to calculate whether something is easy to read
    
    Returns
    -------
    str
        Flesch-Kincaid reading level
    """
    if fs >= 90.:
        return 'Very easy to read'
    elif fs >= 80 and fs < 90:
        return 'Easy to read'
    elif fs >= 70 and fs < 80:
        return 'Fairly easy to read'
    elif fs >=60 and fs < 70:
        return 'Plan English'
    elif fs >=50 and fs < 60:
        return 'Fairly difficult to read'
    elif fs >=30 and fs < 50:
        return 'Difficult to read'
    else:
        return 'Very difficult to read'

def get_recommendations_from_input(txt):
    """
    Cleans, preprocesses, and generates heuristic 
    suggestion for input string
    Parameters
    ----------
    txt: String 
        Input text
    Returns
    -------
        Suggestions for a given text input
    """
    processed = clean_input(txt)
    tokenized_sentences = preprocess_input(processed)
    suggestions = get_suggestions(tokenized_sentences)
    return suggestions


if __name__ == '__main__':
    text = parse_arguments()
    print(get_suggestions(text))