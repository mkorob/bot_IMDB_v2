# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 22:00:47 2022

@author: maria
"""

#### FILE TO RUN FIRST TO LOAD ALL THE GLOBAL VARIABLES
#### PASS THE NAMES OF THE FOLDERS WHERE THEY ARE LOCATED

location_KG = 'C:/Users/maria/Downloads/ddis-movie-graph_nt'
location_emb = 'C:/Users/maria/OneDrive/Documents/GitHub/embeddings/ddis-graph-embeddings'
import setup.setup as setup
setup.initiate(location_KG, location_emb)

# AFTER THIS ALL THE VARIABLES ARE LOADED AND YOU CAN RUN DEMO_AGENT WHENEVER