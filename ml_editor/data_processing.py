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