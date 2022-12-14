# Advanced Techniques in Artificial Intelligence Conversational Agent


This project contains an intelligent conversational agent built as an assingment for the Advanced Topics in Artificial Intelligence course at the University of Zurich.
It is able to answer three types of queries:
* factual questions about properties of movies that are available on Wikidata (e.g. director of Inception)
* movie recommendations based on one or several movies provided by the user.
* image retrieval of one or more actors (if photos of them together exist) from the IMDb database.

## Organisation

### Folders and Structures

Directory is structured as follows:
* *launch.py* - file to be run to load the use data before any agent can initiated)
* *demo_agent.py* - file containing the Speakeasy implementation of the bot
* *test_home.py* - local implementation of the bot with trial questions to test_home
* *setup* package containing the data loaded to be used by the bot (crowd data and relations wikidata) and the setup script that is run in *launch.py*
* *responsebots* package containing the three types of bots used to answer the three kind of questions and the overall receiver (ResponseBotFinal)

Instructions on which files to run for the bot to function can be found below in the relevant section.

### Pre-requisites and imports
Depending on your existing installations, additional installations of packages may be required. Such packages may be, but not limited to: 
* *requests*
* *transformers*
* *rdflib*
* *nltk*
* *Levenshtein*
* *sklearn*
* *urrlib*

Note: there have been reported inconsitencies between inconsistent versions of requests, urrlib and transformers. If issues arise, try uninstalling and reinstalling requests.

### Additional configurations.
This application was developed in Spyer, with User Module Reloader (UMR) disabled. Depending on your Python interpreter, you may need to ensure that your environment does not automatically reload modules on every import.

## How It Works
### Methodology
1. The agent receives the question from the user in *demo_agent.py* and passes it to its individual instance of BotResponseFinal.
2. BotResponseFinal retrives named entities from the question (film names and actors names), Wikidata relation properties and classifies the question as one of the three questions described above usng a custom BERT-based model (see more infromation below) and manual corrections. There are then three options:
  * factual questions are passed to a FactResponse instance with movie names and relationships as parameters, which first tries to look up the query in the knowledge graph, checks that the answer isn't covered by crowd data. If no information is found, it will provide closest guesses from the embedding data.
  Priority is given to crowd data, then to knowledge graph answers, and only finally to embeddings. 
  * recommendation questions are passed to a RecResponse instance with movie names as parameters, where it tries to find most common neighbours of all the movies provided, and returns matches based on 15 most similar movies for each film.
  * image retrieval questions are passed to a MediaResponse instance which looks for an image of all the actors mentioned in the sentence.
  
### Instructions

There are two options of accessing the bot. First is loading the bot to be used in the Speakeasy environment, and the second is to load in a local testing environment.

Speakeasy Way:
1. Define location of the knowledge graph and embedding information in *launch.py* and execute the file.
2. Run demo agent *demo_agent.py*

You should now be able to converse with the *maria.korobeynikova_bot* chatbot in the Speakeasy environment.

Local testing way:
1. Define location of the knowledge graph and embedding information in *test_home.py*
2. Uncomment the question out of list of provided questions by section and run *test_home.py*

   
 ### Notes on the classifier model
 The model used to classify user-typed input into one of the types of question was a customly fine-tuned BERT transformer model by me using a small balanced training dataset of ~50 rows (training and validation data can be found in /classifiermodel/question_builder.xlsx).
 It was trained in the Google Colab notebook found in the same folder and then puushed to Huggingface to my account (mkorob) to be imported in the local installation.
 ```diff
	from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
	tokenizerClass = AutoTokenizer.from_pretrained("mkorob/class-sent")
	modelClass = AutoModelForSequenceClassification.from_pretrained("mkorob/class-sent")
	classSent = pipeline("text-classification", model=modelClass, tokenizer=tokenizerClass)
 ```
 The model has 5 classes: 0 - complicated question (requiring more than one query), 1 - recommendation question, 2 - media question, 3- factual question, 4 - random question (not regarding movies or actors).


