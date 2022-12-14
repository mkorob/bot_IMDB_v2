# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 21:56:53 2022

@author: maria
"""
import rdflib
import setup.setup as setup
from sklearn.metrics import pairwise_distances
from collections import Counter
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
class RecResponse():
    def __init__(self):
        
        self.recommended_prepositors = ["I made some recommendations for you... ",
                                        "So what can I recommend is ",
                                        "I have come up with the following - ",
                                        "Similar movies would be - "]
        
        
    def answer_question(self, movie_names):
        self.movie_names = movie_names
        def list_items_and(list_attr):
            len_list = len(list_attr)
            if len_list > 1:
                pre_join = ", ".join(list_attr[0:(len_list-1)])
                outr = pre_join+" or "+list_attr[len_list-1]
            else:
                outr = list_attr[0]
            return outr
        
        def closest_response(movie_ent_id, no_responses):
            # get embedding of the entity
            ent = setup.ent2id[movie_ent_id]
            # we compare the embedding of the query entity to all other entity embeddings
            dist = pairwise_distances(setup.entity_emb[ent].reshape(1, -1), setup.entity_emb).reshape(-1)
            # order by plausibility
            most_likely = dist.argsort()
            most_likely_entities = [setup.id2ent[idx] for idx in most_likely[:no_responses]]
            #some entities pulled from embeddings don't have labels
            most_likely_labels = [""]*no_responses
            for entix, ent in enumerate(most_likely_entities):
                try:
                    most_likely_labels[entix] = setup.ent2lbl[ent]
                except:
                    most_likely_labels[entix] = ""
            
            top_labels = most_likely_labels[0:no_responses]
            return top_labels
        
        movieids_list = []
        for name in self.movie_names:
            
            #First pull ID anyways - lbl2ent has all entities, e.g. Batman will map to the superhero
            query_ex = """
                     prefix wdt: <http://www.wikidata.org/prop/direct/>
                     prefix wd: <http://www.wikidata.org/entity/>
                     
                     SELECT ?ent ?lbl WHERE {
                         ?ent rdfs:label ?label.
                         ?ent wdt:P31/wdt:P279* wd:Q11424 .
                     }
                     """
            
            #run the query
            qres2 = setup.graph.query(query_ex, initBindings={'label': rdflib.Literal(name, lang = "en")})
            res_dir = {ent for ent, lbl in qres2}
            movie_ids = list(res_dir)
            movieids_list = movieids_list +movie_ids
        
        labels_list = []
        for movieid in movieids_list:
            
            similar_entities = closest_response(movieid, 15)
            labels_list = labels_list + list(similar_entities)
        
        
        if len(self.movie_names) == 1:
            #the first movie is the name of the movie itself
            recommended_movies = labels_list[1:4]
        
        else:
            recommended_movies = []
        #get the first item with maximum occurrences
            counter = Counter(labels_list).most_common()
            #counts = list(counter.values())
            max_count = counter[0][1]
            if max_count > 1:
                for count_pair in counter:
                    if count_pair[1] >1 and count_pair[0] not in self.movie_names:
                         recommended_movies.append(count_pair[0])
                    if len(recommended_movies) == 3:
                         break
        
        #formulate answer
        if len(recommended_movies) == 0:
            response_out = "Seems like you are asking about very different movies.. Can you think of something more similar?"
        else:
            preresp = self.recommended_prepositors[0]
            if len(self.recommended_prepositors)  > 1:
                self.recommended_prepositors = self.recommended_prepositors[1:]
                print(self.recommended_prepositors)
            response_out = preresp+list_items_and(list(set(recommended_movies)))
        return response_out
        