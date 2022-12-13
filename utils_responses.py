# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:37:01 2022

@author: maria
"""

def pop_elements(list_responses):
    resp_out = list_responses[0]
    if len(list_responses) > 1:
        list_responses = list_responses[1:]
    return resp_out

def reduce_list(list_phrases):
     if len(list_phrases) >1:
            list_phrases = list_phrases[1:]
     return list_phrases