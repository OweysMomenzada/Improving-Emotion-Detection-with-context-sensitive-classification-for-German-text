<big><b> Author: Oweys Momenzada </big></b>

# Improving Emotion Detection with context sensitive classification for German text
<big><i> FOR DEEPER INSIGHT INTO THE WORK AND APPROACH, ALL NOTEBOOKS ARE WELL DOCUMENTED AND PROVIDED ON THIS GITHUB REPOSITORY. </i></big>

#### What is this repository about?
In my time at <a href="https://www.schickler.de/">SCHICKLER</a> I was allowed to work on the award-winning <a href="https://www.presseportal.de/pm/8218/4932175">DRIVE</a>-Project.
The Drive project has data from various regional publishers throughout Germany. 
My task was to improve an existing Emotion Classifier used for their dataset on Google BigQuery. In addition, I have also implemented Sentiment Analysis for their dataset which has not been implemented before.

##### What is Emotion Detection/Sentiment Analysis and why is a solution relevant?
Emotion Detection simply detects emotions in a text. For instance, we could detect <i>joy, fear, fear and sadness</i> in our text. With Sentiment Analysis the text can be labeled (most common) as <i>negative, positive or neutral</i>. Which sounds so easy, is actually quite challenging. There is no existing data for German Emotion Detection and also
Sentiment Analysis is poorly documented. With my approach we can actually build a decent Emotion Classifier for German text and could also outperform existing Sentiment Analysis approaches on some cases (such as the <a href="https://huggingface.co/oliverguhr/german-sentiment-bert">Oliverguhr</a> Sentiment Analysis model, which is based on <a href="https://arxiv.org/abs/1810.04805">BERT</a>.).

## Data

As mentioned we do not have any 
