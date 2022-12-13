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
import pandas as pd
from nltk.stem import PorterStemmer
from image_search import MediaResponse
from factresponse import FactResponse
from recresponse import RecResponse
import setup
from Levenshtein import distance as lev
from utils_responses import pop_elements
import itertools


class BotResponseNew:
    def __init__(self, question):
        self.question = question
        self.irrelevant_answers_out = [ "Are we just chatting? I think we don't have time for that, I've got to pass this course...",
                        "I think you aren't asking me about things that I know, please ask me about movies! :)",
                        "This isn't a question about movies or media, is it....?",
                        "Please, we are running out of time for you to ask me things I know about..."
            ]
        
        self.complicated_answers_out = ["This is too hard for me to answer in this time.. Let's start with something simpler",
                                        "This is again too difficult.... Can you ask something more in line with the type of questions we had to prepare?",
                                        ]
        
        self.typos_answers_out = ["I can't find any movie names or actors in your questions... Can you check the spelling?",
                                  "I again can't find any movie names, sorry... Sure everything is spelt correctly?",
                                  "Please check your spelling!"]
        
        
    def answerQuestion(self):
        
        def join_ners(type_ner, nlp_patch):
            types_ner = ["B-"+type_ner, "I-"+type_ner]
            out_array = []
            for ner_r in nlp_patch:
                #get word
                if ner_r['entity'] in types_ner:
                    if ner_r['entity'][0] == "B":
                        out_array.append(ner_r['word'])
                    else:
                        if ner_r['word'][0] == "#":
                            out_array[len(out_array)-1] = out_array[len(out_array)-1]+ner_r['word'][2:]
                        else:
                            out_array[len(out_array)-1] = out_array[len(out_array)-1]+" "+ner_r['word']
                            
            return out_array
  
        # PART 0 - check if there are any NER and People (PER-NER)
        # don't jum the gun because NER is case-sensitive
        ner_results = setup.nlpEnt(self.question)
        names_question = join_ners("PER", ner_results)
        labels = ["comp", "rec", "media", "fact", "random"]
        class_p = labels[int(setup.classSent(self.question)[0]['label'][6])]
        
        #PART 2- find all subsets of words
        question_minus_punct = re.sub(",","", self.question).lower()
        all_spaces = []
        for pos, sentstr in enumerate(question_minus_punct):
            if sentstr ==  " ":
                all_spaces.append(pos)
        
        
        if len(all_spaces) == 0:
            all_subsets = question_minus_punct
        elif len(all_spaces) == 1:
            all_subsets = word_tokenize(question_minus_punct)
        else:
            #add the last point where the 
            last = 0
            for i in range(len(question_minus_punct)):
                if question_minus_punct[i].isalpha():
                    last = i+1
            all_spaces.append(last)
            all_subsets = []
            all_combs = list(itertools.combinations(all_spaces, 2))
            for spacepos in all_combs:
                all_subsets.append(question_minus_punct[(spacepos[0]+1):spacepos[1]])
                #[3, 5, 8, 9, 10]  - 35, 38, 39, 310, 
                
        
        # PART 1- check if there is a movie title in the input or a person
        #print(self.question)
        #match with minimum levenshtein distance 2
        movie_matches_pos = []
        for movie_pos, moviename in enumerate(setup.all_films_names):
            for substrsent in all_subsets:
                if lev(moviename.lower(), substrsent) < (len(substrsent)/20) and substrsent not in stopwords.words('english'):
                    print(moviename+substrsent)
                    movie_matches_pos.append(movie_pos)
                    
        #make sure to not have any obverwrites, e.g. Batman and Batman Returns need to be one only           
        if (movie_matches_pos):
            #select all films that are matched
            all_films_matches = []
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
                    
        #if neither can be found exit
        if len(names_question) == 0 and len(movie_matches_pos) == 0:
            if len(ner_results) == 0 and class_p == "random":
                return pop_elements(self.irrelevant_answers_out)
            else:
                return pop_elements(self.typos_answers_out)
                
        #Part 3 - CLASSIFY QUESTION
        
        #try to find a relation name
        #TODO: add lev distance
        #relation_names_df = pd.read_csv("relations_titles.csv")
        ps = PorterStemmer()
        relation_names = setup.relationData["Label"]
        relations_stem = [ps.stem(rel) for rel in relation_names]
        rel_combo = list(relation_names)+relations_stem
        relation = []
        for word in all_subsets:
            w = ps.stem(word)
            #w_match = [lev(w, rel_c) for rel_c in rel_combo]
            if w in rel_combo:
                print(w)
                #if it's longer than the length of dataframe, subtract length of dataframe
                index_match = rel_combo.index(w)
                if index_match > len(relations_stem):
                    index_match = index_match -len(relations_stem)
                relation = setup.relationData['Relation'][index_match]
                relation_name = setup.relationData['Label_out'][index_match]
                break
        print(len(relation))
    
        #run classifier
        
        # Node 1 - if there are personal names in the question but no movies, it's a media question or "other"
        if class_p == "fact" and len(relation) > 0:
            print("reached fact")
            if len(all_films_matches) == 1:
                class_response = "fact"
            else:
                class_response = "comp"
        
        elif class_p == "media" and len(names_question) > 0:
            print("reached media")
            class_response = "media"
        
        elif class_p == "rec" and len(movie_matches_pos) > 0:
            print("reached rec")
            class_response = "rec"
            
        elif class_p in ["comp", "random"]:
            class_response = "comp"
            
        else:
            response_out = "I am a bit confused by your question... Could you please express yourself differently?"
            return response_out
        
        #assign to a member of a class
        if class_response == "comp":
            return pop_elements(self.complicated_answers_out)
        if class_response == "fact":
            response_query = FactResponse(all_films_matches[0], relation, relation_name)
            
        if class_response == "rec":
            response_query = RecResponse(all_films_matches)
        
        if class_response == "media":
            response_query = MediaResponse(names_question)
    
            
        response_out = response_query.answer_question()
        return response_out