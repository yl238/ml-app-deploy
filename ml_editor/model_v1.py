import os
from pathlib import Path

import pandas as pd
import joblib
from scipy.sparse import vstack, hstack

from ml_editor.data_processing import add_v1_features

FEATURE_ARR = [
    "action_verb_full",
    "question_mark_full",
    "text_len",
    "language_question",
]

curr_path = Path(os.path.dirname(__file__))

model_path = Path('../models/model_1.pkl')
vectorizer_path = Path('../models/vectroizer_1.pkl')

VECTORIZER = joblib.load(curr_path / vectorizer_path)
MODEL = joblib.load(curr_path / model_path)
