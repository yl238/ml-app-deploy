import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from scipy.sparse import vstack, hstack


def format_raw_df(df):
    """Clean up data and join questions to answers
    
    Parameters
    ----------
    df : Pandas DataFrame
        raw DataFrame
    
    Returns:
        processed DataFrame
    """
    # Fixing types and setting index
    df['PostTypeId'] = df['PostTypeId'].astype(int)
    df['Id'] = df['Id'].astype(int)
    df['AnswerCount'].fillna(-1, inplace=True)
    df['AnswerCount'] = df['AnswerCount'].astype(int)
    df['OwnerUserId'].fillna(-1, inplace=True)
    df['OwnerUserId'] = df['OwnerUserId'].astype(int)
    df.set_index('Id', inplace=True, drop=False)

    df['is_question'] = df['PostTypeId'] == 1

    # Filtering out PostTypdIds other than documented ones
    df = df[df['PostTypeId'].isin([1, 2])]

    # Linking questions and answers
    df = df.join(
        df[["Id", "Title", "body_text", "Score", "AcceptedAnswerId"]],
        on='ParentId',
        how='left',
        rsuffix="_question",
    )
    return df


def train_vectorizer(df):
    """
    Train a vectorizer for some data.
    Returns the vectorizer to be used to transform non-training data, in
    addition to the training vectors
    
    Parameters
    ----------
    df : Pandas DataFrame
        data used to train the vectorizer
    """
    vectorizer = TfidfVectorizer(
        strip_accents='ascii', min_df=5, max_df=0.5, max_features=10000
    )
    vectorizer.fit(df["full_text"].copy())
    return vectorizer


def get_vectorized_series(text_series, vectorizer):
    """
    Vectorizes an input series using a pre-trained vectorizer
    
    Parameters
    ----------
    text_series : Pandas Series of text
    vectorizer : pretrained sklearn vectorizer
    """
    vectors = vectorizer.transform(text_series)
    vectorized_series = [vectors[i] for i in range(vectors.shape[0])]
    return vectorized_series


def add_text_features_to_df(df):
    """
    Adds features to DataFrame
    
    Parameters
    ----------
    df : DataFrame
    """
    df['full_text'] = df['Title'].str.cat(df['body_text'], sep=" ", na_rep="")
    df = add_v1_features(df.copy())

    return df


def add_v1_features(df):
    """
    Add our first features to an input DataFrame
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame of questions
    """
    df['action_verb_full'] = (
        df['full_text'].str.contains('can', regex=False)
        | df['full_text'].str.contains('What', regex=False)
        | df['full_text'].str.contains('should', regex=False)
    )
    df["language_question"] = (
        df["full_text"].str.contains("punctuate", regex=False)
        | df["full_text"].str.contains("capitalize", regex=False)
        | df["full_text"].str.contains("abbreviate", regex=False)
    )
    df["question_mark_full"] = df["full_text"].str.contains("?", regex=False)
    df["text_len"] = df["full_text"].str.len()
    return df


def get_vectorized_inputs_and_label(df):
    """
    Concatenate DataFrame features with text vectors.
    Returns concatenated vector consisting of features and text.
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame with calculated features.
    """
    vectorized_features = np.append(
        np.vstack(df['vectors']),
        df[
            [
                "action_verb_full",
                "question_mark_full",
                "norm_text_len",
                "language_question"
            ]
        ],
        1,
    )
    label = df['Score'] > df['Score'].median()
    return vectorized_features, label


def get_feature_vector_and_label(df, feature_names):
    """
    Generate input and output vectors using the vectors feature and
    the given feature names
    
    Parameters
    ----------
    df : Pandas DataFrame
        input dataframe
    feature_names : array
        Names of feature columns (other than vectors)
    """
    vec_features = vstack(df["vectors"])
    num_features = df[feature_names].astype(float)
    features = hstack([vec_features, num_features])
    labels = df['Score'] > df["Score"].median()
    return features, labels


def get_random_train_test_split(posts, test_size=0.3, random_state=42):
    """
    Get train/test split from DataFrame
    Assume the DataFrame has one row per question example

    Parameters
    ----------
    posts : Pandas DataFrame
        All posts with their labels
    test_size : float, optional
        The proportion to allocate to test, by default 0.3
    random_state : int, optional
        random_seed, by default 42
    """
    return train_test_split(
        posts, test_size=test_size, random_state=random_state
    )


def get_split_by_author(
    posts, author_id_column='OwnerUserId', test_size=0.3, random_state=42
):
    """
    Get train/test split
    Guarantee every author only appears in one of the splits
    
    Parameters
    ----------
    posts : Pandas DataFrame
        All posts, with their labels
    author_id_column : str, optional
        Name of the column containing the author_id, by default 'OwnerUserId'
    test_size : float, optional
        The proportion allocated to test, by default 0.3
    random_state : int, optional
        random_state, by default 42
    """
    splitter = GroupShuffleSplit(
        n_splits=1, test_size=test_size, random_state=random_state
    )
    splits = splitter.split(posts, groups=posts[author_id_column])
    train_idx, test_idx = next(splits)
    return posts.iloc[train_idx, :], posts.iloc[test_idx, :]


def get_normalized_series(df, col):
    """
    Get a normalized version of a column
    
    Parameters
    ----------
    df : DataFrame
    col : str
        Column name

    Returns
    -------
        Normalized series using Z-score
    """
    return (df[col] - df[col].mean()) / df[col].std()