# -*- coding: utf-8 -*-
"""
Created on Mon Nov 7 19:17:40 2022

@author: maria
"""
import nltk
import numpy as np
from nltk import word_tokenize
import re
import pickle
import pandas as pd
from nltk.stem import PorterStemmer
from rdflib import URIRef
from rdflib import Literal
from nltk.util import everygrams
from image_search import MediaResponse
from factresponse import FactResponse
from recresponse import RecResponse
import setup


class BotResponse:
    def __init__(self, question):
        self.question = question

        
    def answerQuestion(self):
  
        # PART 0 - IF I HAVE TIME - if the question is not about a movie (falls under a classification "irrelevant"), do an auto-generated response
        #e.g. the answer + "let's talk about movies though!"

        # PART 1- check if there is a movie title in the input or a person
        print(self.question)
        sentence = word_tokenize(self.question)
        names_spl = list(everygrams(sentence, max_len=10))
        names_str = [" ".join(name_spl) for name_spl in names_spl]
        
        #match 
        name = [x in self.question for x in setup.all_films_names]
        #name = [x in setup.all_films_names for x in names_str]
        # if (any(name)):
        #     matches = np.where(name)[0]
        #     movie_rel_name = ""
        #     for match_pos in range(len(matches)):
        #         new_name = names_str[matches[match_pos]]
        #         if len(new_name) > len(movie_rel_name):
        #             movie_rel_name = new_name
        if (any(name)):
            matches = np.where(name)[0]
            # movie_rel_name = ""
            #for match_pos in range(len(matches)):
            #     new_name = setup.all_films_names[matches[match_pos]]
            #     if len(new_name) > len(movie_rel_name):
            #         movie_rel_name = new_name
            
            #select all films that are matched
            all_films_matches = []
            for match_pos in range(len(matches)):
                new_name = setup.all_films_names[matches[match_pos]]
                add_film = True
                #case 1- unrelated so you add
                #case 2 - Batman is stored, and you overwrite with Batman Returns
                #case 3- Batman Returns is there and you don't add
                if len(all_films_matches) > 0:
                    for pos in range(len(all_films_matches)):
                        ex_film = all_films_matches[pos]
                        if ex_film in new_name:
                            all_films_matches[pos] = new_name
                        if new_name in ex_film:
                            add_film = False
                if (add_film):
                    all_films_matches.append(new_name)
            print(all_films_matches)
    
        #person
        ner_results = setup.nlpEnt(self.question)
        def join_ners(type_ner, nlp_patch):
            types_ner = ["B-"+type_ner, "I-"+type_ner]
            out_array = []
            for ner_r in ner_results:
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
        
        names_question = join_ners("PER", ner_results)
        print(names_question)

        #if neither can be found exit
        if len(names_question) == 0 and not (any(name)):
            response_out = "I cannot find any movies or people inside your question... I only talk about these things because everything else is boring. If you are asking me a correct question, try to check your spelling."
            return response_out
       
            
        #import relation names
        relation_names_df = pd.read_csv("relations_titles.csv")
        ps = PorterStemmer()
        relation_names = relation_names_df["Label"]
        relations_stem = [ps.stem(rel) for rel in relation_names]
        rel_combo = list(relation_names)+relations_stem
        for word in names_str:
            w = ps.stem(word)
            if w in rel_combo:
                print(w)
                #if it's longer than the length of dataframe, subtract length of dataframe
                index_match = rel_combo.index(w)
                if index_match > len(relations_stem):
                    index_match = index_match -len(relations_stem)
                relation = relation_names_df['Relation'][index_match]
                relation_name = relation_names_df['Label_out'][index_match]
                break
    
            
        #otherwise, start classifying
        phrases_factquestion = ["Who", "When", "What year", "Where", "direct", "What was"] + list(relation_names)
        phrases_recommend = ["Recommend", "you recommend", "advice", "recommend me", "movies like", "recommendation", "films like", "similar to", "enjoyed", "something"]
        phrases_media = ["Show", "show", "photo", "picture", "to see", "to view", "looks like", "look like"]
        
        # Node 1 - if there are personal names in the question but no movies, it's a media question or "other"
        print("check names")
        print(names_question)
        print("check movies")
        print(any(name))
        if len(names_question) > 0:
              print(names_question)
              #check words of movies
              media = [x in phrases_media for x in names_str]
              if any(media):
                  class_response = "media"
              else:
                  response_out = "I see you are asking me about a person but I can't understand what you want... Can you please rephrase?"
                  return response_out
        else:
            print("not media")
            # Node 2 - if there is a movie name in the question, it's a question or a recommendation
            scores_count = []
            scores_count.append(sum([1 for phrase in phrases_factquestion if phrase in names_str]))
            scores_count.append(sum([1 for phrase in phrases_recommend if phrase in names_str]))
            
            #get all rows where maximum matching
            print(scores_count)
            max_score = [i for i, j in enumerate(scores_count) if j == max(scores_count)]
            
            #find most likely
            if len(max_score) == 1:
                class_response = ["fact", "rec"][max_score[0]]
            
            else:
                response_out = "I am a bit confused by your question... Could you please express yourself differently?"
                return response_out
        
        #assign to a member of a class
        if class_response == "fact":
            response_query = FactResponse(all_films_matches[0], relation, relation_name)
            
        if class_response == "rec":
            response_query = RecResponse(all_films_matches)
        
        if class_response == "media":
            response_query = MediaResponse(names_question)
            
            
        response_out = response_query.answer_question()
        return response_out
   