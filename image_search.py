# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 23:05:21 2022

@author: maria
"""
#from torchvision.io import read_image
import urllib.request, json 
from rdflib import Literal
import setup

link_images = "https://files.ifi.uzh.ch/ddis/teaching/2021/ATAI/dataset/movienet/"
# TODO: move it out to data loading part so it doesn't need to load everytime a question is asked
with urllib.request.urlopen('https://files.ifi.uzh.ch/ddis/teaching/2021/ATAI/dataset/movienet/images.json') as url:
    json_dir = json.load(url)


class MediaResponse:
    def __init__(self, names):
        self.names = names[0]
        
    def answer_question(self):
        
        response_out = "I messed up somewhere.."
        
        #TODO: Check response if more than one matches by name
        query_ex = """
                  prefix wdt: <http://www.wikidata.org/prop/direct/>
                  prefix wd: <http://www.wikidata.org/entity/>
                  
                  SELECT ?ent ?movieid WHERE {
                      ?ent rdfs:label ?label.
                      ?ent wdt:P345 ?movieid.
                  }
                  """
              
        qres2 = setup.graph.query(query_ex, initBindings={'label': Literal(self.names, lang = "en")}) 
    
        imdb_id = [lbl for ent, lbl in qres2]
    
        #TODO: include photos which are multi-cast
        if len(imdb_id) ==1:
            imdb_id = str(imdb_id[0])
            # get first match
            id_photo = ""
            for load in json_dir:
                if load['cast'] == [imdb_id]:
                    id_photo = load['img']
                    break
            #check if there are any matches
            if id_photo == "":
                response_out = "I don't seem to have any photos of "+self.names+" unfortunately... Do you want to see anyone else maybe?"
            else:
                response_out = "image:"+id_photo.split(".")[0]
            
        return response_out
    


