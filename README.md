<big><b> Author: Oweys Momenzada </big></b>

# Improving Emotion Detection with context sensitive classification for German text corpus
<big><i> FOR DEEPER INSIGHT INTO THE WORK AND APPROACH, ALL NOTEBOOKS ARE WELL DOCUMENTED AND PROVIDED ON THIS GITHUB REPOSITORY. </i></big>

#### What is this repository about?
In my time at <a href="https://www.schickler.de/">SCHICKLER</a> I was allowed to work on the award-winning <a href="https://www.presseportal.de/pm/8218/4932175">DRIVE</a>-Project.
The Drive project has data from various regional publishers throughout Germany. 
My task was to improve an existing Emotion Classifier used for their dataset on Google BigQuery. In addition, I have also implemented Sentiment Analysis for their dataset which has not been implemented before.

#### What is Emotion Detection/Sentiment Analysis and why is a solution relevant?
Emotion Detection simply detects emotions in a text. For instance, we could detect <i>joy, fear, fear and sadness</i> in our text. With Sentiment Analysis the text can be labeled (most common) as <i>negative, positive or neutral</i>. Which sounds so easy, is actually quite challenging. There is no existing data for German Emotion Detection and also
Sentiment Analysis is poorly documented. With my approach we can actually build a decent Emotion Classifier for German text and could also outperform existing Sentiment Analysis approaches on some cases (such as the <a href="https://huggingface.co/oliverguhr/german-sentiment-bert">Oliverguhr</a> Sentiment Analysis model, which is based on <a href="https://arxiv.org/abs/1810.04805">BERT</a>.).

#### What is my solution?
Before, SCHICKLER used triggerwords to get emotions from the text. The problem here is that context can not be taken into account. For instance,
"das freut mich gar nicht" (translates to: "I am not pleased at all") would be positive, since the triggerword would be "freuen" (translates to: pleased).
My solution is to train a model on labeled dialogues and example sentences based on the triggerwords (see section <i>Data</i>). The Sentiment are going to be
generated based on negative emotions (fear, anger, sadness) and positive emotions (joy). We also will use a "neutral" emotion to neutralize overloaded emotions. This will be explained in detail in the following sections.

## Data
<big><i>ALL DATA AND FUNCTIONS RELATED TO DATA COLLECTION CAN BE SEEN IN "./Data collecting"</big></i>

As mentioned we do not have any data to implement an Emotion Detection model. Therefore, we need to build a dataset on our own. In the first step we build our dataset based on the triggerwords (for triggerwords, see citation or <i>"./Data collecting/triggerwords.xlsx"</i>). We than send our triggerwords to an API (<a href="https://www.dwds.de/d/api">DWDS-API</a>) and then generate sentences based on these words. This could look as followed: 

![image1](https://github.com/OweysMomenzada/Improving-Emotion-Detection-with-context-sensitive-classification-for-German-text/blob/main/images/image1.png)

We also filter negations to avoid false labeling. In this way we could generate more than 6000 sentences based on 680 triggerwords. However, since this dataset has no
negations, we also use some english dialogues from various datasets (see <i>citation</i>) to solve this issue. We use the Google NLP API (see <i>"./Data collecting/Emotiondataset_builder.py"</i>) to translate the english dataset to german sentences. Finally, we have a dataset with over 11 000 sentences for five emotions: <i>anger, sadness, joy, fear and neutral </i> (see <i>"./Data collecting/fullset.csv"</i>). 

## Model
<big><i>MODEL AND TRAINING CAN BE SEEN IN "./Model training/Model training.ipynb"</big></i>

Since SCHICKLER used triggerwords for detection, the running time was comparatively really fast. This is important, since SCHICKLER is getting a lot of data into their pipelines and therefore a short running time is costly more efficient. Therefore, we need a model which is good in performance and accuracy. In our experiments, we noticed that simple LSTMs are way more efficient in running time (compared to BERT, BiLSTM, CNN+LSTM) and also have a decent accuracy. Because of that, we will use the LSTM model to train.

A prediction on our model could look as follows (For more examples and results see <i>"./Results and Examples.ipynb"</i>):
```
# translated to: Today's weather forecast: there will be a tornado today
predict('Wetterbericht von heute: heute wird es einen Tornado geben')

>>>{'anger': 0.013,
>>>  'fear': 0.9147,
>>>  'joy': 0.0105,
>>>  'neutral': 0.0039,
>>>  'sadness': 0.058}
```

## Sentiment Analysis
The Sentiments are defined as [<i>negative, likely negative, neutral, likely positive</i>] based on the emotions. Negative emotion will output a negative sentiment score and
positive emotions will output a positive sentiment score. For the threshold of each sentiment see <i>"./Application - API/main.py"</i>.

The Sentiment Analysis approach of this work could experimentally outperform state-of-art opensource projects for German Sentiment-Analysis, such as the <a href="https://huggingface.co/oliverguhr/german-sentiment-bert">Oliverguhr</a>-project. 

Finally our results look like this:
```
example = create_emotions_sentiment("Heute spielen FC Bayern gegen den FC Barcelona.")

print(example)

>>>{'emotions': 
>>>  {'anger': 0.0665030256, 
>>>  'fear': 0.1034225, 
>>>  'joy': 0.545249, 
>>>  'neutral': 0.0235871468, 
>>>  'sadness': 0.261238247},
>>>sentiments': 
>>>  {'sentiment_label': 'neutral', 
>>>  'sentiment_valence': 0.0905028532}}
```


## Real world Application, API & Deployment
A Real World Application on some Headliners of articles can be seen here "Results and Examples.ipynb"

We provide this for the SCHICKLERS database on an API. We first store the trained model into a Bucket in Google Cloud Storage and than load it into GCP AI Platform. We then implement Textcleaning and other Feature Engineering steps and also the communcation with the trained model on AI platform on a different .py-file (see "<i>"./Application - API/main.py"</i>"). In addition, we use FLASK for our RESTful API. We implement a POST request to send requests to the API. We then finally deploy our API on APP Engine to provide for EDA purposes and our dataset.

&nbsp;

![Workflow](https://github.com/OweysMomenzada/Evergreen-Content-Classifier-for-german-Text/blob/main/EDA/images/Worfklow.png)

## Citation
#### Used Datasets
- <b>dailydialog</b>: 2017, 102k <br>
- <b>emotion-stimulus</b>: 2015<br>
- <b>isear</b>:	1990	<br>

##### Used triggerwords
``` 
@book{aschenbrenner2019emotionserkennung,
  title={Emotionserkennung bei Nachrichtenkommentaren mittels Convolutional Neural Networks und Label Propagationsverfahren},
  author={Aschenbrenner, A. and Spies, M.},
  url={https://core.ac.uk/download/pdf/275811762.pdf},
  year={2019},
  publisher={Universit{\"a}tsbibliothek der Ludwig-Maximilians-Universit{\"a}t},
  pages={339-352}
}

```


Please cite this GitHub if you use this work.
```
@misc{momenzada_schickler_2021_emotion, 
      title={Improving Emotion Detection with context sensitive classification for German text corpus}, 
      author={Momenzada, Oweys and SCHICKLER}, 
      url={https://github.com/OweysMomenzada/Improving-Emotion-Detection-with-context-sensitive-classification-for-German-text-corpus}, 
      journal={Github}, 
      year={2021}, 
      month={Sep}
      } 
```

