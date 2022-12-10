# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 16:57:58 2022

@author: maria
"""
## This file processes the crowd data used to augment the agent

!python -m pip install statsmodels
import pandas as pd
import numpy as np
import statsmodels as sm
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
from rdflib import URIRef

########
# %% Load Data and Inspect
crowd_data = pd.read_table("crowd_data.tsv")
#everyone received the same reward
#everyone's assignment status is submitted
#crowd_data[['WorkerId','LifetimeApprovalRate'] ].groupby(['LifetimeApprovalRate']).count().plot()
#most popular approval rates are 40% and 98%

# %% Filter out illegible users
# Concept: filter out users with too low rating (below 50%) and answer too quickly

# I first checked mean response by question - overall people take about 100 seconds to answer a question and min time is 40, so I would filter anyone who answers below 40
# t = crowd_data.groupby(['HITId'])[['WorkTimeInSeconds']].mean().sort_values('WorkTimeInSeconds').plot.bar()

# Here, I checked the users and filtered out all below 50 seconds per tak (the edge-case of 40% had a low approval rate)
t = crowd_data.groupby(['WorkerId', 'LifetimeApprovalRate'])[['WorkTimeInSeconds']].mean().sort_values('WorkTimeInSeconds').reset_index()
invalid_worker_ids = t['WorkerId'][(t['WorkTimeInSeconds'] < 100) | (t['LifetimeApprovalRate'] == "40%")].values

crowd_data_filt = crowd_data[~crowd_data['WorkerId'].isin(invalid_worker_ids)]

# %% Prepare 
answers = crowd_data_filt.groupby(['HITId', 'HITTypeId','Input1ID', 'Input2ID', 'Input3ID', 'AnswerLabel'])['WorkerId'].count().reset_index()
answers_dist =  answers.pivot(index = ["HITId", "HITTypeId", 'Input1ID', 'Input2ID', 'Input3ID'], columns = "AnswerLabel", values = "WorkerId")
answers_dist = answers_dist.replace(np. nan,0)
answers_dist.to_excel("answers_distribution.xlsx")
answers_values = crowd_data_filt.groupby(["HITId", "FixPosition", "FixValue"])['WorkerId'].count().reset_index()
#remove a fake one, otherwise every other question has only one answer
answers_values = answers_values[answers_values['FixPosition'] != "2"]

def apply_fleiss(datachunk):
    out = sm.stats.inter_rater.fleiss_kappa(datachunk, method='fleiss')
    return out

#find inter-agreement rate per batch
inter_agreements = answers_dist.groupby('HITTypeId').apply(apply_fleiss).reset_index()
answers_dist = answers_dist.reset_index()

#get questions
def get_entity(text):
    out = text
    if isinstance(text, str):
        if ":" in text:
            entities = text.split(":")
            if entities[0] == "wd":
                out = URIRef(WD+entities[1])
            elif entities[0] == "wdt":
                out = URIRef(WDT+entities[1])
            else:
                out = text
    else:
        out = "nan"    
    return out



def get_ent_lab(text):
    if  not isinstance(text, float):
        if text[0:4] == "http":
            try:
                out = setup.ent2lbl[text]
            except:
                out = "not found"
        else:
            out = text
    else:
        out = "nan"
    return out


answers_dist['entity'] = answers_dist['Input1ID'].apply(get_entity)
answers_dist['relation'] = answers_dist['Input2ID'].apply(get_entity)
answers_dist['answer'] = answers_dist['Input3ID'].apply(get_entity)
#answers_dist['rel_lab'] = answers_dist['Input2ID'].apply(get_number)
answers_dist['entity_lab'] = answers_dist['entity'].apply(get_ent_lab)
answers_dist['answer_lab'] = answers_dist['answer'].apply(get_ent_lab)
#add inter-agreemetn 
answers_dist = answers_dist.merge(inter_agreements, left_on = "HITTypeId", right_on = "HITTypeId", how = "left")
answers_dist = answers_dist.merge(answers_values, left_on = "HITId", right_on = "HITId", how = "left")
answers_dist['FixResponse'] = answers_dist['FixValue'].apply(get_entity)
answers_dist['FixResponse'] = answers_dist['FixResponse'].apply(get_ent_lab)
answers_dist['FixResponse'][answers_dist['FixPosition'] == "Predicate"] = [URIRef(WDT+answer) for answer in answers_dist['FixValue'][answers_dist['FixPosition'] == "Predicate"]]
#ent2lbl[URIRef(WD+answers_dist['entity_number'][1])]

        
#What is the birthplace of Christopher Nolan? 
#Agent: London - according to the crowd, who had an inter-rater agreement of 0.72 in this batch. 
#The answer distribution for this specific task was 2 support votes and 1 reject vote.

#get final answer
#TODO: IMPORTANT - some answers are properties, but right now they are coded as strings
answers_dist['final_answer'] = answers_dist['answer_lab']
answers_dist['final_answer'][answers_dist['INCORRECT'] > 1] = answers_dist['FixResponse'][answers_dist['INCORRECT'] > 1]
answers_dist['final_answer'][answers_dist['FixResponse'] == "nan"] = answers_dist['answer_lab'][answers_dist['FixResponse'] == "nan"]
#get number of responders
answers_dist['no_answers'] = answers_dist['CORRECT']
answers_dist['no_answers'][answers_dist['final_answer'] == answers_dist['FixResponse']] = answers_dist['INCORRECT'][answers_dist['final_answer'] == answers_dist['FixResponse']]

answers_dist.to_excel("crowd_data_processed.xlsx")
global answersDist
answersDist = answers_dist
 

    
