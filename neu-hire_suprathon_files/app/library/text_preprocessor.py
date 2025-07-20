# text_preprocessor.py
# ✨ Cleaned-up NLTK-based text preprocessing module for NeuHire – removes stopwords, punctuation, and lemmatizes tokens.

import re
import string
import pickle
from nltk import pos_tag, wordpunct_tokenize, sent_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords as sw, wordnet as wn
from sklearn.base import BaseEstimator, TransformerMixin

class NLTKPreprocessor(BaseEstimator, TransformerMixin):
    """
    NLTK-based text preprocessor for tokenization, lemmatization, and basic cleaning.
    """

    def __init__(self, max_sentence_len=300, stopwords=None, punct=None, lower=True, strip=True):
        self.lower = lower
        self.strip = strip
        self.max_sentence_len = max_sentence_len
        self.stopwords = set(stopwords) if stopwords else set(sw.words('english'))
        self.punct = set(punct) if punct else set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self.tokenize(doc) for doc in X]

    def tokenize(self, text):
        tokens = []

        # Clean text with basic substitutions
        text = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", text)
        text = re.sub(r"\s{2,}", " ", text).strip().lower()

        for sent in sent_tokenize(text):
            for word, tag in pos_tag(wordpunct_tokenize(sent)):
                word = word.lower().strip(string.punctuation) if self.lower else word
                if word in self.stopwords or all(c in self.punct for c in word):
                    continue
                lemma = self.lemmatize(word, tag)
                tokens.append(lemma)

        return ' '.join(tokens)

    def lemmatize(self, token, tag):
        tag_dict = {'N': wn.NOUN, 'V': wn.VERB, 'R': wn.ADV, 'J': wn.ADJ}
        return self.lemmatizer.lemmatize(token, tag_dict.get(tag[0], wn.NOUN))
