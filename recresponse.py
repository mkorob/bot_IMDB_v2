# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 21:56:53 2022

@author: maria
"""
import rdflib
import setup
from sklearn.metrics import pairwise_distances
import pandas as pd
import numpy as np
from collections import Counter
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
class RecResponse():
    def __init__(self, movie_names):
        self.movie_names = movie_names
        
        
    def answer_question(self):
        def list_items_and(list_attr):
            len_list = len(list_attr)
            if len_list > 1:
                pre_join = ", ".join(list_attr[0:(len_list-1)])
                list_attr = pre_join+" and "+list_attr[len_list-1]
            return list_attr
        
        def closest_response(movie_name, no_responses):
            # get embedding of the entity
            ent = setup.ent2id[setup.lbl2ent[movie_name]]
            # we compare the embedding of the query entity to all other entity embeddings
            dist = pairwise_distances(setup.entity_emb[ent].reshape(1, -1), setup.entity_emb).reshape(-1)
            # order by plausibility
            most_likely = dist.argsort()
            most_likely_entities = [setup.id2ent[idx] for idx in most_likely[:10]]
            #some entities pulled from embeddings don't have labels
            most_likely_labels = [""]*10
            for entix, ent in enumerate(most_likely_entities):
                try:
                    most_likely_labels[entix] = setup.ent2lbl[ent]
                except:
                    most_likely_labels[entix] = ""
            
            # df_results = pd.DataFrame([
            #     (
            #         setup.id2ent[idx][len(WD):], # qid
            #         setup.ent2lbl[setup.id2ent[idx]],  # label
            #         dist[idx],             # score
            #         rank+1,                # rank
            #     )
            #     for rank, idx in enumerate(most_likely[:15])],
            #     columns=('Entity', 'Label', 'Score', 'Rank'))
            
            top_labels = most_likely_labels[0:no_responses]
            #top_labels = np.unique(df_results['Label'][0:min(no_responses, len(df_results))].values)
            return top_labels
        
        labels_list = []
        for name in self.movie_names:
            similar_entities = closest_response(name, 10)
            labels_list = labels_list + list(similar_entities)
        
        if len(self.movie_names) == 1:
            recommended_movies = labels_list[0:3]
        
        else:
            recommended_movies = []
        #get the first item with maximum occurrences
            counter = Counter(labels_list)
            counts = list(counter.values())
            max_count = max(counts)
            if max_count > 1:
                for idx, count_key in enumerate(list(counter.keys())):
                    if counts[idx] == max_count and count_key not in self.movie_names:
                        recommended_movies.append(count_key)
                    if len(recommended_movies) == 3:
                        break
        
        #formulate answer
        if len(recommended_movies) == 0:
            response_out = "Seems like you are asking about very different movies.. Can you think of something more similar?"
        else:
            response_out = "I made some recommendations for you... "+list_items_and(recommended_movies)
            
        return response_out
        