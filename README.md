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
<big><i>ALL DATA AND FUNCTIONS CAN BE SEEN IN (.......)</big></i>

As mentioned we do not have any data to implement an Emotion Detection model. Therefore, we need to build a dataset on our own. In the first step we build our dataset based on the triggerwords (for triggerwords, see citation or /..........!!!!!). We than send our triggerwords to an API (<a href="https://www.dwds.de/d/api">DWDS-API</a>) and then generate sentences based on these words. This could look as followed: 

![image1](https://github.com/OweysMomenzada/Improving-Emotion-Detection-with-context-sensitive-classification-for-German-text/blob/main/images/image1.png)

We also filter negations to avoid false labeling. In this way we could generate more than 6000 sentences based on 680 triggerwords. However, since this dataset has no
negations, we also use some english dialogues from various datasets (see <i>citation</i>) to solve this issue. We use the Google NLP API (see ....) to translate the english dataset to german sentences. Finally, we have a dataset with over 11 000 sentences for five emotions: <i>anger, sadness, joy, fear and neutral </i> (see .....). 

## Model
<big><i>MODEL AND TRAINING CAN BE SEEN IN (.......)</big></i>

Since SCHICKLER used triggerwords for detection, the running time was comparatively really fast. This is important, since SCHICKLER is getting a lot of data into their pipelines and therefore a short running time is costly more efficient. Therefore, we need a model which is good in performance and accuracy. In our experiments, we noticed that simple LSTMs are way more efficient in running time (compared to BERT, BiLSTM, CNN+LSTM) and also have a decent accuracy. 

A prediction on our model could look as follows (For more examples and results see....):
```
# translated to: Today's weather forecast: there will be a tornado today
predict('Wetterbericht von heute: heute wird es einen Tornado geben')

>>>{'anger': 0.013,
>>>  'fear': 0.9147,
>>>  'joy': 0.0105,
>>>  'neutral': 0.0039,
>>>  'sadness': 0.058}
```
