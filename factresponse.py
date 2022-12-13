# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 23:25:13 2022

@author: maria
"""
import rdflib
from rdflib import URIRef
from rdflib import Literal
import setup
from sklearn.metrics import pairwise_distances
import pandas as pd
import numpy as np
from utils_responses import pop_elements

WD = rdflib.Namespace('http://www.wikidata.org/entity/')

#TODO: maybe initiate with an ID
class FactResponse():
    def __init__(self, movie_name, relation_urlstr, relation_name):
        self.movie_name = movie_name
        self.relation_urlstr = URIRef(relation_urlstr)
        self.relation_name = relation_name
        self.bad_answers_out = [ "Sorry, I don't have this kind of information... Do you want to know anything else?",
                         "Again, you are asking for something I have no information on... Let's try something else!",
                         "Wow, you are very unlucky! You keep asking questions about the gaps in my data...",
                         "No information again..."]
        
   
    
    def answer_question(self):
        
        def give_response(entity, relation):
            
            #TODO: rename 0
            #find row
            answer_row = setup.crowdData[['final_answer', 'no_answers', 0]][(setup.crowdData['entity'] == entity) & (setup.crowdData['relation'] == relation)]
            #if not found, return "not found"
            if len(answer_row) == 0:
                return "none"
                exit()
                
            #otherwise get 
            answer = answer_row['final_answer'].values[0]
            votes = answer_row['no_answers'].values[0]
            irr_agreement = round(answer_row[0].values[0], 2)
            
            
            if votes > 1:
                response_out = "So this answer was actually improved by our reviewers, who said that the correct answer is "+answer+ ". This was agreed by "+str(int(votes))+ " out of 3 voters who had an inter-rater agreement of "+ str(irr_agreement)+ "."
            else:
                response_out = "So my response is "+ answer+ ", but "+ str(int(3-votes))+ " out of 3 of my human reviewers who have an inter-rater of agreement of "+str(irr_agreement)+ " told me that this answer is wrong.... They didn't have any better suggestions though, so there you go!"
                
            return response_out
        
        def list_items_and(list_attr, prepositor):
            len_list = len(list_attr)
            pre_join = ", ".join(list_attr[0:(len_list-1)])
            return pre_join+prepositor+list_attr[len_list-1]
        
        def closest_response(entity, relation, no_responses):
            #check if relation is in the embedding data (e.g. box office or year are not)
            if relation in setup.all_embed_relations:
            # get embedding of the entity
                head = setup.entity_emb[setup.ent2id[entity]]
                pred = setup.relation_emb[setup.rel2id[relation]]
                lhs = head + pred
                dist = pairwise_distances(lhs.reshape(1, -1), setup.entity_emb).reshape(-1)
                most_likely = dist.argsort()
                most_likely_entities = [setup.id2ent[idx] for idx in most_likely[:10]]
                #some entities pulled from embeddings don't have labels
                most_likely_labels = [""]*10
                for entix, ent in enumerate(most_likely_entities):
                    try:
                        most_likely_labels[entix] = setup.ent2lbl[ent]
                    except:
                        most_likely_labels[entix] = ""
            #     df_results = pd.DataFrame([
            # (setup.id2ent[idx][len(WD):], setup.ent2lbl[setup.id2ent[idx]], dist[idx], rank+1)
            # for rank, idx in enumerate(most_likely[:10])],
            # columns=('Entity', 'Label', 'Score', 'Rank'))
                #select top three labels
                #top_three_labels = np.unique(df_results['Label'][0:no_responses].values)
                top_three_labels = most_likely_labels[0:no_responses]
                return top_three_labels
            else:
                return []
        

        #1. Pull all names    
        query_ex = """
                 prefix wdt: <http://www.wikidata.org/prop/direct/>
                 prefix wd: <http://www.wikidata.org/entity/>
                 
                 SELECT ?ent ?lbl WHERE {
                     ?ent rdfs:label ?label.
                     ?ent wdt:P31/wdt:P279* wd:Q11424 .
                     ?ent ?relation ?obj .
                     ?obj rdfs:label ?lbl.
                 }
                 """
    
        
        #run the query
        qres2 = setup.graph.query(query_ex, initBindings={'label': Literal(self.movie_name, lang = "en"), 'relation':self.relation_urlstr})
        res_dir = {ent[31:]: str(lbl) for ent, lbl in qres2}
        
        #print all entities (for my info)
        print(res_dir)
        
        #check here for enrichment with data
        if len(res_dir) == 0:
            #get at least one entity from the array
            movie_ent_id = setup.lbl2ent[self.movie_name]
            #first try crowd data
            response_crowd = give_response(movie_ent_id, self.relation_urlstr)
            if response_crowd != "none":
                return response_crowd
            
            #get closest responses
            embedding_answers = closest_response(movie_ent_id, self.relation_urlstr, 3)
            if len(embedding_answers) > 0:
                response_out = "I don't know the exact answer, but I've analyzed similar movies and I think the answer should be "+list_items_and(embedding_answers, " or ")
            else:
                response_out = pop_elements(self.bad_answers_out)
            #TODO: check in embeddings
            return response_out
        
        
        
        else:
            #WD = rdflib.Namespace('http://www.wikidata.org/entity/')
            ents = list(res_dir.keys())
            
            #try a crowd data response for any of the entities
            for movie_ent in ents:
                ent = URIRef(WD+movie_ent)
                print(ent)
                response_crowd = give_response(ent, self.relation_urlstr)
                if response_crowd != "none":
                    return response_crowd
            
            #TODO: find package to return plural of the word?
            if len(res_dir) == 1:
                response_out ="The "+self.relation_name +" of "+ self.movie_name + " is " +list(res_dir.values())[0]
            else:
                response_out = "There are " + str(len(res_dir))+ " films in the database under this name. Their " + self.relation_name+"s are "+list_items_and(list(res_dir.values()), " and ")
            
            return response_out
            

        
        