import os
from pathlib import Path

import spacy
import joblib
from tqdm import tqdm
import pandas as pd 
import nltk
from scipy.sparse import vstack, hstack

nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

POS_NAMES = {
    "ADJ": "adjective",
    "ADP": "adposition",
    "ADV": "adverb",
    "AUX": "auxiliary verb",
    "CONJ": "coordinating conjunction",
    "DET": "determiner",
    "INTJ": "interjection",
    "NOUN": "noun",
    "NUM": "numeral",
    "PART": "particle",
    "PRON": "pronoun",
    "PROPN": "proper noun",
    "PUNCT": "punctuation",
    "SCONJ": "subordinating conjunction",
    "SYM": "sumbol",
    "VERB": "verb",
    "X": "other",
}

FEATURE_ARR = [
    "num_questions",
    "num_periods",
    "num_commas",
    "num_exclam",
    "num_quotes",
    "num_colon",
    "num_stops",
    "num_semicolon",
    "num_words",
    "num_chars",
    "num_diff_words",
    "avg_word_len",
    "polarity"
]
FEATURE_ARR.extend(POS_NAMES.keys())

SPACY_MODEL = spacy.load("en_core_web_md")
tqdm.pandas()

curr_path = Path(os.path.dirname(__file__))

model_path = Path('../models/model_2.pkl')
vectorizer_path = Path("../models/vectorizer_2.pkl")
VECTORIZER = joblib.load(curr_path / vectorizer_path)
MODEL = joblib.load(curr_path / model_path)


def count_each_pos(df):
    """
    Count occurrences of each part of speech, and add it to an input DataFrame.
    
    Parameters
    ----------
    df : Pandas DataFrame
        Input DataFrame containing text that has been passed to SPACY_MODEL
    Returns
    -------
        DataFrame with occurrence counts
    """
    global POS_NAMES
    pos_list = df["spacy_text"].apply(lambda doc: [token.pos_ for token in doc])
    for pos_name in POS_NAMES.keys():
        df[pos_name] = (
            pos_list.apply(
                lambda x: len([match for match in x if match == pos_name])
            )
            / df["num_chars"]
        )
    return df


def get_word_stats(df):
    """
    Adds statistical features such as word counts to a DataFrame
    
    Parameters
    ----------
    df : DataFrame
        Containing full_text column with training questions.

    Returns
    -------
        DataFrame with new feature columns
    """
    global SPACY_MODEL
    df['spacy_text'] = df['full_text'].progress_apply(
        lambda x: SPACY_MODEL(x))

    df['num_words'] = (
        df["spacy_text"].apply(lambda x: 100 * len(x)) / df["num_chars"]
    )
    df["num_diff_words"] = df["spacy_text"].apply(lambda x: len(set(x)))
    df["avg_word_len"] = df["spacy_text"].apply(lambda x: get_avg_word_len(x))

    df["num_stops"] = (
        df["spacy_text"].apply(
            lambda x: 100*len([stop for stop in x if stop.is_stop])
        )
        / df["num_chars"]
    )

    df = count_each_pos(df.copy())
    return df


def get_avg_word_len(tokens):
    """
    Returns average word length for a list of words
    
    Parameters
    ----------
    tokens : array-like
        List of words
    """
    if len(tokens) < 1:
        return 0
    lens = [len(x) for x in tokens]
    return float(sum(lens) / len(lens))


def add_char_count_features(df):
    """
    Adds counts of punctuation characters to a DataFrame
    
    Parameters
    ----------
    df : DataFrame 
        Containing a full_text column with training questions
    
    Returns
    -------
        DataFrame with counts
    """
    df["num_chars"] = df["full_text"].str.len()

    df["num_questions"] = 100 * df["full_text"].str.count("\?") / df["num_chars"]
    df["num_periods"] = 100 * df["full_text"].str.count("\.") / df["num_chars"]
    df["num_commas"] = 100 * df["full_text"].str.count(",") / df["num_chars"]
    df["num_exclam"] = 100 * df["full_text"].str.count("!") / df["num_chars"]
    df["num_quotes"] = 100 * df["full_text"].str.count('"') / df["num_chars"]
    df["num_colon"] = 100 * df["full_text"].str.count(":") / df["num_chars"]
    df["num_semicolon"] = 100 * df["full_text"].str.count(";") / df["num_chars"]
    return df


def get_sentiment_score(df):
    """
    Uses nltk to return a polarity score for an input question
    
    Parameters
    ----------
    df : DataFrame
        Contains a full_text column with training questions.

    Returns
    ------
        DataFrame with a polarity column.
    """
    sid = SentimentIntensityAnalyzer()
    df["polarity"] = df["full_text"].progress_apply(
        lambda x: sid.polarity_scores(x)["pos"]
    )
    return df


def add_v2_text_features(df):
    """
    Adds multiple features used by the v2 model to a DataFrame.
    
    Parameters
    ----------
    df : DataFrame
        Containing a full_text column with training questions.

    Returns
    -------
        DataFrame with feature columns added
    """
    df = add_char_count_features(df.copy())
    df = get_word_stats(df.copy())
    df = get_sentiment_score(df.copy())
    return df


def get_model_probabilities_for_input_texts(text_array):
    """
    Returns an array of probability scores representing
    the likelihood of a question receiving a high score
    format is: [ [prob_low_score_1, prob_high_score_1], ...]
    
    Parameters
    ----------
    text_array : array-like
        Array of questions to be scored

    Returns
    -------
        array of predicted probabilities
    """
    global FEATURE_ARR, VECTORIZER, MODEL
    vectors = VECTORIZER.transform(text_array)
    text_ser = pd.DataFrame(text_array, columns=["full_text"])
    text_ser = add_v2_text_features(text_ser.copy())
    vec_features = vstack(vectors)
    num_features = text_ser[FEATURE_ARR].astype(float)
    features = hstack([vec_features, num_features])
    return MODEL.predict_proba(features)


def get_question_score_from_input(text):
    """
    Helper method to get the probability for the positive class
    for one example question
    
    Parameters
    ----------
    text : string
        Text to get the probability of positive class
    
    Returns
    -------
        Estimated probability of question receiving a high score
    """
    preds = get_model_probabilities_for_input_texts([text])
    positive_proba = preds[0][1]
    return positive_proba


def get_pos_score_from_text(input_text):
    """
    Get a score that can be displayed in the Flask app
    
    Parameters
    ----------
    input_text : String
        Input text
    
    Returns
    -------
        Estimated probability of question receiving a high score
    """
    positive_proba = get_question_score_from_input(input_text)
    output_str = (
        """
        Question score (0 is worst, 1 is best):
        <br/>
        {}
        """.format(positive_proba)
    )
    return output_str