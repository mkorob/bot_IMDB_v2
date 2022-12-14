# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 23:05:21 2022

@author: maria
"""
#from torchvision.io import read_image
#import urllib.request, json 
from rdflib import Literal
import setup

link_images = "https://files.ifi.uzh.ch/ddis/teaching/2021/ATAI/dataset/movienet/"


class MediaResponse:
    def __init__(self):
        self.answers_out = ["I don't seem to have any photos of "]
        
    def answer_question(self, names):
        self.names = names
        response_out = "I messed up somewhere.."
        
        names_out = []
        for name in self.names:
        
    #TODO: Check response if more than one matches by name
            query_ex = """
                      prefix wdt: <http://www.wikidata.org/prop/direct/>
                      prefix wd: <http://www.wikidata.org/entity/>
                      
                      SELECT ?ent ?movieid WHERE {
                          ?ent rdfs:label ?label.
                          ?ent wdt:P345 ?movieid.
                      }
                      """
                  
            qres2 = setup.graph.query(query_ex, initBindings={'label': Literal(name, lang = "en")}) 
        
            imdb_id = [str(movieid) for ent, movieid in qres2]
            if len(imdb_id) > 0:
                 names_out.append(imdb_id[0])
    
        
        if len(names_out) == 0:
              return "I can't find an actor ID in my database unfortunately... Can you check the name spelling?"
        
        print(names_out)
        id_photo = ""
        if len(self.names) ==1:
            for load in setup.json_dir:
               if load['cast'] == names_out:
                   id_photo = load['img']
                   break
        #only run this if more than one person or you can't find an image of just one person
        if len(self.names) > 1 or id_photo == "":
            for load in setup.json_dir:
              if set(names_out).issubset(set(load['cast'])):
                  id_photo = load['img']
                  break
        #check if there are any matches
        if id_photo == "":
            if len(self.names) == 1:
                response_out = self.answers_out[0]+self.names+" unfortunately... Do you want to see anyone else maybe?"
            else:
                response_out = "I don't have a photo of them together.. Ask for a photo of just one of them!"
        else:
            response_out = "image:"+id_photo.split(".")[0]
            
        return response_out
    


