# speech_emotion_recognition.py
# ✨ Simplified Speech Emotion Recognition module for NeuHire – credits to original CNN+LSTM SER architectures.

import numpy as np
import librosa
from scipy.stats import zscore
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Dense, Dropout, Activation, TimeDistributed,
    Conv2D, MaxPooling2D, BatchNormalization, Flatten, LSTM
)

class SpeechEmotionRecognition:
    def __init__(self, model_weights=None):
        self._emotion = {
            0: 'Angry', 1: 'Disgust', 2: 'Fear',
            3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'
        }
        if model_weights:
            self._model = self._build_model()
            self._model.load_weights(model_weights)

    def _mel_spectrogram(self, y, sr=16000):
        mel = np.abs(librosa.stft(y, n_fft=512, hop_length=128)) ** 2
        mel = librosa.feature.melspectrogram(S=mel, sr=sr, n_mels=128, fmax=4000)
        return librosa.power_to_db(mel, ref=np.max)

    def _frame(self, y, win_step=64, win_size=128):
        nb_frames = 1 + int((y.shape[2] - win_size) / win_step)
        frames = np.zeros((y.shape[0], nb_frames, y.shape[1], win_size)).astype(np.float16)
        for t in range(nb_frames):
            frames[:, t, :, :] = np.copy(y[:, :, t * win_step:t * win_step + win_size])
        return frames

    def _build_model(self):
        K.clear_session()
        input_y = Input(shape=(5, 128, 128, 1), name='Input')
        y = TimeDistributed(Conv2D(64, (3, 3), padding='same'))(input_y)
        y = TimeDistributed(BatchNormalization())(y)
        y = TimeDistributed(Activation('elu'))(y)
        y = TimeDistributed(MaxPooling2D((2, 2), padding='same'))(y)
        y = TimeDistributed(Dropout(0.2))(y)

        y = TimeDistributed(Flatten())(y)
        y = LSTM(128, return_sequences=False, dropout=0.2)(y)
        output = Dense(7, activation='softmax')(y)
        return Model(inputs=input_y, outputs=output)

    def predict(self, filename, sample_rate=16000):
        y, sr = librosa.load(filename, sr=sample_rate, offset=0.5)
        chunks = self._frame(y.reshape(1, 1, -1), 16000, 49100).reshape(-1, 49100)
        norm_chunks = np.asarray([zscore(c) for c in chunks])
        mel = np.asarray([self._mel_spectrogram(c) for c in norm_chunks])
        X = self._frame(mel).reshape(mel.shape[0], 5, 128, 128, 1)
        pred = self._model.predict(X)
        return [self._emotion[np.argmax(p)] for p in pred]
