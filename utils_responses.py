# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:37:01 2022

@author: maria
"""

def pop_elements(list_responses):
    if len(list_responses) > 1:
        resp_out = list_responses.pop(0)
    else:
        resp_out = list_responses[0]
    return resp_out