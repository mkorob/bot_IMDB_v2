# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 19:56:04 2022

@author: maria
"""
import setup
setup.init()
from botresponse import BotResponse
message = "Who directed Inception?"
message = "Who directed The Bridge on the River Kwai?"

#run by parts
#Question 1 - Factual Question
message = "Who directed The Bridge on the River Kwai?"
message = "Who is the director of Star Wars: Episode VI - Return of the Jedi?"
message = "Who is the director of Star Wars: Episode VI – Return of the Jedi?"
message = "What is the genre of Shrek the Third?"
botresponse = BotResponse(str(message))
response = botresponse.answerQuestion()
print(response)

message = "What does Julia Roberts look like?"

#run by parts
#Question 2 - Media Question
botresponse = BotResponse(str(message))
response = botresponse.answerQuestion()
print(response)

#run by parts
#Question 3 - Crowdsourced Question
message = "What was the production company of Mulan?"
message = "Who is the executive producer of X-Men: First Class?"
botresponse = BotResponse(str(message))
response = botresponse.answerQuestion()
print(response)

#Question 4 - Embedding Question
message = "What is the genre of Good Neighbors?"
botresponse = BotResponse(str(message))
response = botresponse.answerQuestion()
print(response)

#Question 5- Recommending Questions
message = "Given that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?"
#message = "Recommend me movies like Shrek the Third"
botresponse = BotResponse(str(message))
response = botresponse.answerQuestion()
print(response)


###NOTES
# questions not working
#Who is the director of Star Wars: Episode VI - Return of the Jedi?

