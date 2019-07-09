import nltk
nltk.download("stopwords")
nltk.download("punkt")

import string
import operator

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer


langdetect_to_nltk = {
    "da" : "danish",
    "fi" : "finnish",
    "el": "greek",
    "it": "italian",
    "no": "norwegian",
    "ru": "russian",
    "sv": "swedish",
    "ar": "arabic",
    "nl": "dutch",
    "fr": "french",
    "hu": "hungarian",
    "pt": "portuguese",
    "sl": "slovene",
    "en": "english",
    "de": "german",
    "id": "indonesian",
    "ne": "nepali",
    "ro": "romanian",
    "es": "spanish",
    "tr": "turkish",
}


def get_features(text):
    try:
        langdetect_language_code = detect(text)
    except LangDetectException:
        langdetect_language_code = "en"
    nltk_language_code = langdetect_to_nltk.get(langdetect_language_code, "english")
    stop_words = set(nltk.corpus.stopwords.words(nltk_language_code))

    tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words=stop_words)
    try:
        tfs = tfidf.fit_transform([text])
    except ValueError:
        return [], [], 0


    feature_names = tfidf.get_feature_names()
    features = dict()
    for col in tfs.nonzero()[1]:
        features[feature_names[col]] = tfs[0, col]
    features_scores_sorted = sorted(features.items(), key=operator.itemgetter(1))
    features = []
    scores = []
    total_score = 0
    for feature, score in features_scores_sorted:
        # Remove weird features
        for c in string.punctuation:
            if c in feature:
                break
        else:
            features.append(feature)
            scores.append(score)
            total_score += score
    return features, scores, total_score
    

def score(proposed_text, target_text):
    features_proposed, _, _ = get_features(proposed_text)
    features_target, scores, achieveable_score = get_features(target_text)

    missing_features = []
    existing_features = []
    achieved_score = 0
    for feature, score in zip(features_target, scores):
        if feature in features_proposed:
            achieved_score += score
            existing_features.append(feature)
        else:
            missing_features.append(feature)
    return existing_features, missing_features, achieved_score, achieveable_score
