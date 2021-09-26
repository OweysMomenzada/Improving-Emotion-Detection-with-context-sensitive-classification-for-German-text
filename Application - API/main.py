import googleapiclient.discovery
from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from flask import Flask, render_template, request, abort, jsonify
import re
import pandas as pd
import numpy as np
import pickle

MAX_NB_WORDS = 15000
MAX_SEQUENCE_LENGTH = 150
HIDDEN_DIM = 150
TOKENIZER = Tokenizer(num_words=MAX_NB_WORDS, lower=True)
X = np.load('sentiment.npy')

PROJECT_ID = "project_id"
MODEL_NAME = "model_name"
VERSION_NAME = "v1"
REGION = "europe-west1"
PROJECT = 'project_name'
KEY_PATH = "credentials.json"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def get_json():
    if request.method == "POST":
        if request.json:
            request_json = request.json
            if 'text' in request_json:
                json_result = get_results(request_json['text'])
                return jsonify(json_result)
            abort(400, 'JSON data missing text field.')
        abort(415)
    abort(405)


def get_tokens():
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer_load = pickle.load(handle)

    return tokenizer_load


def clean_text(text):
    text = re.sub('[»„‘’“”…]', ' ', text)
    text = re.sub('\w*\d\w*', 'Nummer', text)
    text = re.sub(r"https?://\S+|www\.\S+", ' ', text)
    text = re.sub('[\u0080-\uffff]w{1-3}', " ", text)
    text = re.sub(r"[^\x00-\x7F\w{1,3}]+", ' ', text)
    text = re.sub(r"(#[\d\w\.]+)", ' ', text)
    text = re.sub(r"(@[\d\w\.]+)", ' ', text)

    tokenizer = get_tokens()

    text = tokenizer.texts_to_sequences([text])

    return text


def predict_json(instances, project=PROJECT, region=REGION, model=MODEL_NAME, version=VERSION_NAME):
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options, credentials=credentials)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']


def neutralize_score(sentiment_val, neutral_score):
    # positive sentiment
    if sentiment_val > 0:
        if sentiment_val > neutral_score:
            return sentiment_val - neutral_score
        else:
            return 0
    
    # negative sentiment
    else:
        if abs(sentiment_val) > neutral_score:
            return sentiment_val + neutral_score
        else: return 0
        

def get_sentiment(pred):
    sentiment = sum([-(pred['anger']),-(pred['fear']),-(pred['sadness']),pred['joy']])
    sentiment_val = np.round(sentiment,5)
    sentiment_val = neutralize_score(sentiment_val, pred['neutral'])
    
    if sentiment_val <= -0.25 and  sentiment_val >= -0.5:
        return  {"sentiment_valence":sentiment_val,  "sentiment_label":"likely negative"}
    
    elif sentiment_val <= -0.5:
        return  {"sentiment_valence":sentiment_val,  "sentiment_label":"negative"}
    
    elif sentiment_val >= 0.25 and  sentiment_val <= 0.5:
        return  {"sentiment_valence":sentiment_val, "sentiment_label":"likely positive"}
    
    elif sentiment_val >= 0.5:
        return  {"sentiment_valence":sentiment_val, "sentiment_label":"positive"}
    
    else:
        return  {"sentiment_valence": sentiment_val, "sentiment_label":"neutral"}

    
def get_if_truncated(text):
    word_list = text.split()
    number_of_words = len(word_list)

    return number_of_words > MAX_SEQUENCE_LENGTH
    
    
def get_results(text):
    is_truncated = get_if_truncated(text)
    text = clean_text(text)
    padded = pad_sequences(text, maxlen=MAX_SEQUENCE_LENGTH)
    json_pred = predict_json(padded.tolist()) 

    emotions_prediction = {'anger': json_pred[0][0], 'fear': json_pred[0][1],
                           'joy': json_pred[0][2], 'neutral': json_pred[0][3],
                           'sadness': json_pred[0][4]}
    
    sentiments_prediction = get_sentiment(emotions_prediction)
    
    results = {
        "sentiments": sentiments_prediction,
        "emotions": emotions_prediction,
        "is_truncated": is_truncated
    }
    
    return results


if __name__=="__main__":
    app.run(port=9000, debug = True)