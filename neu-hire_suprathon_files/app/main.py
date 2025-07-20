"""
main.py — NeuHire: AI-Powered Interview Evaluation System 🧠🎙️
This is an **incomplete prototype** built for SuPrathon 2025 Hackathon – AI/ML Domain.
It performs preliminary analysis on candidate interview responses using audio/text input,
including emotion recognition and personality prediction.

Team: SoloSync | Developer: Swayam Sharma
"""

# === Core Imports ===
from __future__ import division
import os, time, re
import numpy as np
import pandas as pd
from collections import Counter
from nltk import *
from flask import Flask, render_template, session, request, redirect, flash
from werkzeug.utils import secure_filename
import tempfile

# === Audio & Emotion Analysis ===
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play
from playsound import playsound
from library.speech_emotion_recognition import speechEmotionRecognition

# === Text & Personality Analysis ===
from library.text_emotion_recognition import predict
from library.text_preprocessor import NLTKPreprocessor
from tika import parser; import tika; tika.initVM()

# === App Configuration ===
app = Flask(__name__)
app.secret_key = b'(\xee\x00\xd4\xce"\xcf\xe8@\r\xde\xfc\xbdJ\x08W'
app.config['UPLOAD_FOLDER'] = '/Upload'

# === Global Session Variables ===
global name, duration, job_position, text
tempdirectory = tempfile.gettempdir()

# === Static Routes ===
@app.route('/')
def home(): return render_template('home.html')

@app.route('/about')
def about(): return render_template('about.html')

@app.route('/blogs')
def blogs(): return render_template('blogs.html')

@app.route('/blog_content')
def blog_content(): return render_template('blogs_content.html')

@app.route('/platform', methods=['GET', 'POST'])
def platform(): return render_template('platform.html')

@app.route('/score', methods=['GET', 'POST'])
def score(): return render_template('scorehome.html')

# === Interview Text Entry ===
@app.route('/interview_text', methods=['GET', 'POST'])
def interview_text():
    global name, job_position, duration
    if request.method == 'POST':
        name = request.form['name']
        duration = int(request.form['duration'])
        job_position = request.form['position']
    return render_template('interview_text.html')

# === Interview Answer Text Handler ===
@app.route('/interview', methods=['GET', 'POST'])
def interview():
    global text
    text = request.form['answer']
    flash(f"You will get {duration} sec to answer the question.")
    return render_template('interview.html', name=name, display_button=False, color='#C7EEFF')

# === Record Interview Response ===
@app.route('/audio_recording_interview', methods=['GET', 'POST'])
def audio_recording_interview():
    global duration, text
    sound_path = 'tmp/voice_recording.wav'
    SER = speechEmotionRecognition()
    SER.voice_recording(sound_path, duration=duration)

    r = sr.Recognizer()
    with sr.AudioFile(sound_path) as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source)
            text += r.recognize_google(audio)
        except Exception as e:
            print(e)

    flash("Recording over! Response converted to text.")
    return render_template('interview.html', display_button=True, name=name, text=text, color='#00ffad')

# === Personality & Emotion Scoring Logic ===
@app.route('/interview_analysis', methods=['GET', 'POST'])
def interview_analysis():
    global text, name, job_position
    SER = speechEmotionRecognition(os.path.join('Models', 'audio.hdf5'))
    rec_path = 'tmp/voice_recording.wav'
    emotions, _ = SER.predict_emotion_from_file(rec_path, chunk_step=16000)

    # Save emotion results
    SER.prediction_to_csv(emotions, "static/js/db/audio_emotions.txt", 'w')
    SER.prediction_to_csv(emotions, "static/js/db/audio_emotions_other.txt", 'a')
    major_emotion = max(set(emotions), key=emotions.count)

    # Emotion Distributions
    emo_values = list(SER._emotion.values())
    dist = [int(100 * emotions.count(e) / len(emotions)) for e in emo_values]
    pd.DataFrame(dist, index=emo_values, columns=["VALUE"]).to_csv("static/js/db/audio_emotions_dist.txt")

    # Compare with others
    df_other = pd.read_csv("static/js/db/audio_emotions_other.txt")
    dist_other = [int(100 * len(df_other[df_other.EMOTION == e]) / len(df_other)) for e in emo_values]
    pd.DataFrame(dist_other, index=emo_values, columns=["VALUE"]).to_csv("static/js/db/audio_emotions_dist_other.txt")

    # Personality Prediction from text
    traits = ['Extraversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
    probas = predict().run(text, "Personality_traits_NN")[0].tolist()
    probas_percent = [int(p * 100) for p in probas]
    trait_max = traits[probas_percent.index(max(probas_percent))]

    # Save personality data
    df_old = pd.read_csv('static/js/db/text.txt')
    df_new = df_old.append(pd.DataFrame([probas], columns=traits))
    df_new.to_csv('static/js/db/text.txt', index=False)

    # Save text info
    words = wordpunct_tokenize(NLTKPreprocessor().transform([text])[0])
    counts = Counter(words)
    num_words = len(text.split())
    with open("static/js/db/words_perso.txt", "w") as f:
        f.write("WORDS,FREQ\n")
        for w in counts: f.write(f"{w},{counts[w]}\n")

    # Predict Final Score
    import pickle
    a_score = pickle.load(open('Models/audio_score.sav', 'rb')).predict([dist])[0]
    t_score = pickle.load(open('Models/text_score.sav', 'rb')).predict([probas_percent])[0]
    final_score = round(0.73755 * a_score + 0.262445 * t_score, 2)

    return render_template('score_analysis.html',
                           a_emo=major_emotion,
                           a_prob=dist,
                           t_text=text,
                           t_traits=probas_percent,
                           t_trait=trait_max,
                           t_num_words=num_words,
                           t_common_words=list(counts.keys())[:15],
                           name=name,
                           position=job_position,
                           score=final_score)

# === Text Interview Interface ===
@app.route('/text', methods=['GET', 'POST'])
def text_page(): return render_template('text.html')

@app.route('/text_analysis', methods=['POST'])
def text_analysis():
    raw_text = request.form.get('text')
    return handle_text_analysis(raw_text)

@app.route('/text_input', methods=['POST'])
def text_pdf():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    raw_text = parser.from_file(f.filename)['content']
    return handle_text_analysis(raw_text)

# === Helper Function for Text Personality Analysis ===
def handle_text_analysis(text):
    traits = ['Extraversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']
    probas = predict().run(text, "Personality_traits_NN")[0].tolist()
    probas_percent = [int(p * 100) for p in probas]
    trait_max = traits[probas_percent.index(max(probas_percent))]

    # Save data
    df_old = pd.read_csv('static/js/db/text.txt')
    df_new = df_old.append(pd.DataFrame([probas], columns=traits))
    df_new.to_csv('static/js/db/text.txt', index=False)

    words = wordpunct_tokenize(NLTKPreprocessor().transform([text])[0])
    counts = Counter(words)
    num_words = len(text.split())

    # Save words data
    with open("static/js/db/words_perso.txt", "w") as f:
        f.write("WORDS,FREQ\n")
        for w in counts: f.write(f"{w},{counts[w]}\n")

    return render_template('text_dash.html',
                           traits=probas_percent,
                           trait=trait_max,
                           probas_others=[int(df_new[t].mean() * 100) for t in traits],
                           trait_others=df_new.mean().idxmax(),
                           num_words=num_words,
                           common_words=list(counts.keys())[:15],
                           common_words_others=[])

# === Run the App ===
if __name__ == '__main__':
    app.run(debug=True)
