# Advanced Techniques in Artificial Intelligence Conversational Agent


This project contains an intelligent conversational agent built as an assingment for the Advanced Topics in Artificial Intelligence course at the University of Zurich.
It is able to answer three types of queries:
* factual questions about properties of movies that are available on Wikidata (e.g. director of Inception)
* movie recommendations based on one or several movies provided by the user.
* image retrieval of one or more actors (if photos of them together exist) from the IMDb database.

### Organisation

## How It Works
### Methodology

There are two options of accessing the bot. First is loading the bot to be used in the Speakeasy environment, and the second is to load in a local testing environment.

Speakeasy Way:
1. Define location of the knowledge graph and embedding information in *launch.py* and execute the file.
2. Run demo agent *demo_agent.py*

You should now be able to converse with maria.korobeynikova_bot chatbot in the Speakeasy environment.

Local testing way:
1. Define location of the knowledge graph and embedding information in *test_home.py*
2. Uncomment the question out of list of provided questions by section and run *test_home.py*

   
 ### Notes on classifier Model
 The model used to classify user-typed input into one of the types of question was a customly fine-tuned BERT transformer model by me using a small balanced training dataset of ~50 rows (training and validation data can be found in /classifiermodel/question_builder.xlsx).
 It was trained in the Google Colab notebook found in the same folder and then puushed to Huggingface to my account (mkorob) to be imported in the local installation.
 ```diff
	from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
	tokenizerClass = AutoTokenizer.from_pretrained("mkorob/class-sent")
	modelClass = AutoModelForSequenceClassification.from_pretrained("mkorob/class-sent")
	classSent = pipeline("text-classification", model=modelClass, tokenizer=tokenizerClass)
 ```
 The model has 5 classes: 0 - complicated question (requiring more than one query), 1 - recommendation question, 2 - media question, 3- factual question, 4 - random question (not regarding movies or actors).




const webpackPlugin = require('@size-limit/webpack')

sizeLimit([filePlugin, webpackPlugin], [filePath]).then(result => {
  result //=> { size: 12480 }
})
```
