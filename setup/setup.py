# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 19:19:12 2022

@author: maria
"""
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
import csv
import numpy as np
import rdflib
import pandas as pd
from rdflib import URIRef


#start up the project - load data and initialize pretrained models
def initiate(location_KG, location_emb):
    global graph
    global lbl2ent
    global ent2lbl
    global rel2id
    global id2rel
    global ent2id
    global id2ent
    global entity_emb
    global relation_emb
    global all_films_names
    global all_actors_names
    global all_embed_relations
    global nlpEnt
    global crowdData
    global relationData
    global tokenizerClass
    global classSent
    global json_dir
    global namesPersons
    
    #1 - load Data
    RDFS = rdflib.namespace.RDFS
    
    # load the graph
    graph = rdflib.Graph().parse(location_KG+'/14_graph.nt', format='turtle')
    
    # load embeddings
    entity_emb = np.load(location_emb+'/entity_embeds.npy')
    relation_emb = np.load(location_emb+'/relation_embeds.npy')
    
    #load dictionaries
    with open(location_emb+'/entity_ids.del', 'r') as ifile:
        ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
        id2ent = {v: k for k, v in ent2id.items()}
    with open(location_emb+'/relation_ids.del', 'r') as ifile:
        rel2id = {rdflib.term.URIRef(rel): int(idx) for idx, rel in csv.reader(ifile, delimiter='\t')}
        id2rel = {v: k for k, v in rel2id.items()}
    
    ent2lbl = {ent: str(lbl) for ent, lbl in graph.subject_objects(RDFS.label)}
    lbl2ent = {lbl: ent for ent, lbl in ent2lbl.items()}

    #triples = {(s, p, o) for s,p,o in graph.triples((None, None, None)) if isinstance(o, rdflib.term.URIRef)}
    
    #3. Load names of all movies to parse the question
    all_movies = set(graph.query('''
  prefix wdt: <http://www.wikidata.org/prop/direct/>
  prefix wd: <http://www.wikidata.org/entity/>

  SELECT ?ent ?lbl WHERE {
     ?ent rdfs:label ?lbl.
     ?ent wdt:P31/wdt:P279* wd:Q11424 .
  }
  '''))
 
    all_films_names_nonunique = [str(lbl) for ent, lbl in all_movies]
    all_films_names = list(set(all_films_names_nonunique))
    
    #manually remove films that are causing erros
    all_films_names.remove("The Box")
    all_films_names.remove("Office")
    all_films_names.remove("Image")
    all_films_names.remove("Look")
    all_films_names.remove("Tell")
    all_films_names.remove("Company")
    all_films_names.remove("Play")

    # 2 - BERT NER model loading
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    
    nlpEnt = pipeline("ner", model=model, tokenizer=tokenizer)
    
    # # 4 - Prepare relation names for embedding questions
    all_embed_relations = list(rel2id.keys())
   
    ## 5 - Load crowd data
    crowd_data = pd.read_excel("setup/crowd_data_processed.xlsx")
    #convert all links to URIref
    def convert_links_to_ent(text):
        if(text[0:4] == "http"):
            text = URIRef(text)
        return text
        
    crowd_data['entity'] = crowd_data['entity'].apply(convert_links_to_ent)
    crowd_data['relation'] = crowd_data['relation'].apply(convert_links_to_ent)
    crowd_data['final_answer'] = crowd_data['final_answer'].apply(convert_links_to_ent)
    crowdData = crowd_data
    
    #6 - Classifier model loading
    tokenizerClass = AutoTokenizer.from_pretrained("mkorob/class-sent")
    modelClass = AutoModelForSequenceClassification.from_pretrained("mkorob/class-sent")
    classSent = pipeline("text-classification", model=modelClass, tokenizer=tokenizerClass)
    
    #7 - Relation names
    relationData = pd.read_csv("setup/relations_titles.csv")
    
    #8 - Image data
    import urllib.request, json 
    with urllib.request.urlopen('https://files.ifi.uzh.ch/ddis/teaching/2021/ATAI/dataset/movienet/images.json') as url:
        json_dir = json.load(url)
        
    #10 - Load all cast
    all_actors = set(graph.query('''
  prefix wdt: <http://www.wikidata.org/prop/direct/>
  prefix wd: <http://www.wikidata.org/entity/>

  SELECT ?act ?lbl WHERE {
     ?ent wdt:P31/wdt:P279* wd:Q11424 .
     ?ent wdt:P161 ?act .
     ?act rdfs:label ?lbl.
  }
  '''))
 
    all_actors_names_nonunique = [str(lbl) for ent, lbl in all_actors]
    all_actors_names_un = list(set(all_actors_names_nonunique))
    all_actors_names = [act for act in all_actors_names_un if " " in act] 

    
   
