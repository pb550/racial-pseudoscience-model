# required libraries
import random
import sys
import string
import pandas as pd
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
import seaborn as sns
sns.set('talk')
sns.set_style('ticks')

# define an albert barbasi model
N_people  = 1000 # this is the 'n'
N_follows = 2  # this is the 'm'

np.random.seed(50)
G = nx.barabasi_albert_graph(N_people, N_follows)

# Initial meme simulation
wc = 0.5
wnc = 0.5
meme_init = 50
meme_init_dict = {'meme': [], 'type': [], 'weight': []}
for i in range(1,meme_init+1):
    meme_init_dict['meme'].append(i)
    meme_init_dict['type'].append(random.choices(['C', 'NC'], weights = [wc, wnc])[0])
    if meme_init_dict['type'][i-1] == 'C':
        meme_init_dict['weight'].append(wc)
    else:
        meme_init_dict['weight'].append(wnc)
total_memes = 5000
meme_dict = {'meme': [], 'type': [], 'weight': []}
for i in range(1,total_memes+1):
    meme_dict['meme'].append(i)
    meme_dict['type'].append(random.choices(['C', 'NC'], weights = [wc, wnc])[0])
    if meme_dict['type'][i-1] == 'C':
        meme_dict['weight'].append(wc)
    else:
        meme_dict['weight'].append(wnc)
        
        
agent_posted = 0
pn = 0.45 
pm = 0.4 
pr = 0.029
pnc = 0.5
N = 5          # number of past times to observe contentious memes
time_steps = 60
attn_time = 7
meme_data = {"agent": [], "meme": [], "type": [], "time": [], "state": [], "weight": [], "prob_share": []}
screen_data = {'agent': [], 'sr_meme': [], 'sr_type': [], 'sr_weight': [], 'sr_follows': [], 'sr_time_cur': [], 'sr_time_meme': []}

