# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 15:12:45 2022

@author: maria
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 7 19:17:40 2022

@author: maria
"""
from nltk.corpus import stopwords
from nltk import word_tokenize
import re
from nltk.stem import PorterStemmer
import setup.setup as setup
from Levenshtein import distance as lev
from responsebots.utils_responses import reduce_list
import itertools


class BotResponseFinal:
    def __init__(self, factresponse, mediaresponse, recresponse):
        
        #0. initiate the classes passed as parameters
        self.factresponse = factresponse
        self.mediaresponse = mediaresponse
        self.recresponse = recresponse
        
        #0a. start the arrays of sample responses to parse through to imitate more natural sspeech
        self.irrelevant_answers_out = [ "Are we just chatting? I think we don't have time for that, I've got to pass this course...",
                        "I think you aren't asking me about things that I know, please ask me about movies! :)",
                        "This isn't a question about movies or media, is it....?",
                        "Please, we are running out of time for you to ask me things I know about..."
            ]
        
        self.complicated_answers_out = ["This is too hard for me to answer in this time.. Let's start with something simpler",
                                        "This is again too difficult.... Can you ask something more in line with the type of questions we had to prepare?",
                                        ]
        
        self.typos_answers_out = ["I am a bit confused by your question... Could you please express yourself differently?",
                                  "I can't find enough entities in your questions... Can you check the spelling?",
                                  "I again can't find enough information, sorry... Sure everything is spelt correctly?",
                                  "Please check your spelling!"]
        
        
    def answerQuestion(self, question):
        
        #input question
        self.question = question
       
      
        #try:
        #PART A - GENERATE FEATURES AND BERT CLASSIFY
        
        #POINT 1- convert phrase to lowercase in case people don't capitalize
        question_minus_punct = re.sub(",","", self.question).lower()
        
        #remove just the last punctuation to keep things like E.T. intact
        all_spaces = []
        for pos, sentstr in enumerate(question_minus_punct):
            if sentstr ==  " ":
                all_spaces.append(pos)
        
        last = 0
        for i in range(len(question_minus_punct)):
            if question_minus_punct[i].isalpha():
                last = i+1
                
        #sample greetings to return
        politenesses = {"hello":"Hey!",
               "hey": "Good morning!",
               "hi": "Hey - what can I help with?",
               "thank you": "No problem!",
               "thank you very much": "My pleasure!",
               "thanks": "Cheers!",
               "cheers": "Cheerios!",
               "goodbye": "See you!",
               "how are you": "Good, but let's talk about movies!",
               "bye": "Bye!"}
         
        #POINT 2- CHECK IF IT'S JUST A SMALL GREETING
        #if the whole sentence is just any of these small greetings, return a greeting back- END
        if question_minus_punct[0:last] in list(politenesses.keys()):
                 return politenesses[question_minus_punct[0:last]]
        
        #OTHERWISE CONTINUE
        #POINT 3- GENERATE ALL SUBSETS OF LOWERCASE WORDS
        if len(all_spaces) == 0:
            all_subsets = question_minus_punct
        elif len(all_spaces) == 1:
            all_subsets = word_tokenize(question_minus_punct)
        else:
            #add the last point where the 
            all_spaces.append(last)
            all_subsets = []
            all_combs = list(itertools.combinations(all_spaces, 2))
            for spacepos in all_combs:
                all_subsets.append(question_minus_punct[(spacepos[0]+1):spacepos[1]])
                #[3, 5, 8, 9, 10]  - 35, 38, 39, 310, 
           
        
        # POINT 4- EXTRACT MOVIE NAMES
        #print(self.question)
        #match with minimum levenshtein distance 2
        movie_matches_pos = []
        for movie_pos, moviename in enumerate(setup.all_films_names):
            for substrsent in all_subsets:
                if lev(moviename.lower(), substrsent) < (len(substrsent)/20) and substrsent not in stopwords.words('english'):
                    
                    movie_matches_pos.append(movie_pos)
                    
        #make sure to not have any obverwrites, e.g. Batman and Batman Returns need to be one only           
        all_films_matches = []
        if (movie_matches_pos):
            #select all films that are matched
            for match_pos in range(len(movie_matches_pos)):
                new_name = setup.all_films_names[movie_matches_pos[match_pos]]
                add_film = True
                #case 1- unrelated so you add
                #case 2 - Batman is stored, and you overwrite with Batman Returns
                #case 3- Batman Returns is there and you don't add
                if len(all_films_matches) > 0:
                    for pos in range(len(all_films_matches)):
                        ex_film = all_films_matches[pos].lower()
                        if ex_film in new_name.lower():
                            all_films_matches[pos] = new_name
                        if new_name.lower() in ex_film.lower():
                            add_film = False
                #if it's a one word thing make sure it's a word and not a substring
                if (add_film):
                    all_films_matches.append(new_name)
            all_films_matches = list(set(all_films_matches))
            print(all_films_matches)
            
        #POINT 5 - EXTRACT ACTOR NAMES
        # NER had to be scrapped because it doesn't want to accept Meryl Streep
        names_question = []
        names_typed_q = []
        for subset in all_subsets:
            for actname in setup.all_actors_names:
                if lev(actname.lower(), subset) < 2 and len(actname) > 3 and actname not in names_question:
                    names_question.append(actname)
                    names_typed_q.append(subset)
        print(names_question)
        
        #clean string for classification
        
        class_str = self.question.lower()
        if len(names_question) > 0:
            for nam in names_typed_q:
                class_str = re.sub(nam, "_person_", class_str)
                
        if len(movie_matches_pos) >0:
            for mov in all_films_matches:
                class_str = re.sub(mov.lower(), "_movie_", class_str)
            
        
        #POINT 6- RUN CLASSIFIER 
        print(class_str)
        labels = ["comp", "rec", "media", "fact", "random"]
        class_p = labels[int(setup.classSent(class_str)[0]['label'][6])]
        print(class_p)
        
        #POINT 7 - RUN A GENERIC NER
        #run on capitalized sentence as it's case sensitive
        ner_results = setup.nlpEnt(self.question)
        #names_question = join_ners("PER", ner_results)
  
        #POINT 8 - EXTRACT RELATION NAMES
        
        #try to find a relation name
        ps = PorterStemmer()
        relation_names = setup.relationData["Label"]
        relations_stem = [ps.stem(rel) for rel in relation_names]
        rel_combo = list(relation_names)+relations_stem
        relation = []
        for word in all_subsets:
            w = ps.stem(word)
            #w_match = [lev(w, rel_c) for rel_c in rel_combo]
            if w in rel_combo:
                
                #if it's longer than the length of dataframe, subtract length of dataframe
                index_match = rel_combo.index(w)
                if index_match > len(relations_stem):
                    index_match = index_match -len(relations_stem)
                relation = setup.relationData['Relation'][index_match]
                relation_name = setup.relationData['Label_out'][index_match]
                print(relation_name)
                break
            
        # PART B - DECISION RULES TO FINETUNE CLASS
        class_response = class_p
        print("class predicted")
        print(class_p)
        print("movies")
        print(len(movie_matches_pos))
        print("relation")
        print(len(relation))
        print("actors")
        print(len(names_question))
        
        #Correction 1- if recommendation but no movies, something went wrong
        if class_p == "rec" and len(movie_matches_pos) == 0:
            class_response = "confused"
            
        #Correction 2 - if media but not names, something went wrong
        if class_p == "media" and len(names_question) == 0:
            class_response = "confused"
            
        #Correction 3 - if it's random (like how are you doing), but there are some relevant things then correct
        if class_response == "random" and (len(names_question) > 0 or len(all_films_matches) > 0  or len(ner_results) > 0):
            class_response = "comp"
            
        #Correction 4- if it's fact but there are more than one movie or actor names then it's complicated
        # specifying here both parameters because 
        if class_response == "fact" and (len(all_films_matches) > 1 or len(names_question) > 0):
            class_response = "comp"
        
        #Correction 5 - if it's fact but there isn't a movie and relation then something's wrong
        if class_response == "fact" and (len(all_films_matches) == 0 or len(relation) == 0):
            class_response = "confused"
            
        #Correction 6 - if it's rec but there is one movie and a relation it's a fact
        if class_response == "rec" and len(relation) > 0 and len(all_films_matches) == 1:
            class_response = "fact"
 
        
        #assign to a member of a class
        if class_response == "comp":
            response_out = self.complicated_answers_out[0]
            self.complicated_answers_out = reduce_list(self.complicated_answers_out)
            
        if class_response == "confused":
            response_out = self.typos_answers_out[0]
            self.typos_answers_out = reduce_list(self.typos_answers_out)
            
        if class_response == "fact":
            response_out = self.factresponse.answer_question(all_films_matches[0], relation, relation_name)
            
        if class_response == "rec":
            response_out = self.recresponse.answer_question(all_films_matches)
        
        if class_response == "media":
            response_out = self.mediaresponse.answer_question(names_question)
            
        if class_response == "random":
            response_out = self.irrelevant_answers_out[0]
            self.irrelevant_answers_out = reduce_list(self.irrelevant_answers_out)
    
            
        return response_out
        #except:
        #    return "I am having some issue processing your query, sorry!"