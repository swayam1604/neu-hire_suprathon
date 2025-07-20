# text_emotion_recognition.py
# ✨ Simplified text-based emotion prediction module for NeuHire – using pre-trained RNN models with NLTK preprocessing.

import re
import string
import pickle
import numpy as np
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
from nltk import pos_tag, wordpunct_tokenize, sent_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords as sw, wordnet as wn

class TextEmotionPredictor:
    def __init__(self, model_path='Models/Personality_traits_NN', max_len=300):
        self.max_len = max_len
        self.tokenizer_path = 'Models/padding.pickle'
        self.emotions = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

        # Load model
        with open(model_path + '.json', 'r') as f:
            self.model = model_from_json(f.read())
        self.model.load_weights(model_path + '.h5')
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Load tokenizer
        with open(self.tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)

        # NLP tools
        self.stopwords = set(sw.words('english'))
        self.punct = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()

    def _clean_text(self, text):
        text = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", text)
        text = re.sub(r"\s{2,}", " ", text)
        return text.strip().lower()

    def _lemmatize(self, token, tag):
        tag_dict = {'N': wn.NOUN, 'V': wn.VERB, 'R': wn.ADV, 'J': wn.ADJ}
        return self.lemmatizer.lemmatize(token, tag_dict.get(tag[0], wn.NOUN))

    def _preprocess(self, text):
        tokens = []
        for sent in sent_tokenize(self._clean_text(text)):
            for word, tag in pos_tag(wordpunct_tokenize(sent)):
                word = word.lower().strip(string.punctuation)
                if word in self.stopwords or not word:
                    continue
                lemma = self._lemmatize(word, tag)
                tokens.append(lemma)
        return ' '.join(tokens)

    def predict(self, text):
        cleaned = self._preprocess(text)
        seq = self.tokenizer.texts_to_sequences([cleaned])
        padded = pad_sequences(seq, maxlen=self.max_len, padding='pre', truncating='pre')
        preds = self.model.predict(padded)[0]
        result = dict(zip(self.emotions, preds))
        return result
