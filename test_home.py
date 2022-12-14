# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 19:56:04 2022

@author: maria
"""

### THIS IS A TEST FILE WHERE YOU CAN RUN QUESTIONS WITHOUT LAUNCHING THE BOT

#1. Initialize variables
location_KG = 'C:/Users/maria/Downloads/ddis-movie-graph_nt'
location_emb = 'C:/Users/maria/OneDrive/Documents/GitHub/embeddings/ddis-graph-embeddings'
from setup import setup
setup.initiate(location_KG, location_emb)

#2. Initialize response bots
from responsebots.botresponsefinal import BotResponseFinal
from responsebots.recresponse import RecResponse
from responsebots.factresponse import FactResponse
from responsebots.image_search import MediaResponse
recresponse = RecResponse()
mediaresponse = MediaResponse()
factresponse = FactResponse()
botresponse = BotResponseFinal(factresponse, mediaresponse, recresponse)

#3. Specify message (uncomment the one of interest)

# #a- factual question 
# message = "Who directed Inception?"
# message = "Who directed The Bridge on the River Kwai?"
# message = "Who is the director of Star Wars: Episode VI – Return of the Jedi?"
# message = "What is the genre of Shrek?"
# message = "What is the genre of The silence of the lambs?"
# message = "Hey, can you tell me what is the genre of The silence of the lambs?"
# message = "What is the eirin rating of the wolf of wall streeet" #with a typo
# #b- media question
# #with small typo
# message = "Show me an image of orlando bloom and johny depp"
# message = "Show me an image of Sandra Oh"

message = "What does Julia Roberts look like?"
message = "how are you?"
# message = "Hey, can you tell me what is the genre of The silence of the lambs?"

# #c- recommendation questions
# message = "Given that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?"
# message = "Recommend me movies like Joker and Batman Returns"

# #d - embedding questions
# message = "What is the box office of Finding Dory?" #should return nothing


# #e- crowdsourcing questions
# message = "What was the production company of Mulan?" #BUG
# message = "What was the box office of the Princess and the frog?"

# #f - questions with a typo
# message = "Can you show me a photo of Angelinaaa Evangelista"

# #g- questions which are too complicated for the assignment
# message = "Who does Sarah Jessica Parker play in the jungle book"

#message = "who directed inception"
response = botresponse.answerQuestion(message)
print(response)

