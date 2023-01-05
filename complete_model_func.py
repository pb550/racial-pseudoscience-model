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

N_people = 1000
N_follows = 2
wc = 0.2
wnc = 0.8
meme_init = 50
total_memes = 1500
pn = 0.45 
pm = 0.4 
pr = 0.029
pnc = wnc
N = 5          # number of past times to observe contentious memes
time_steps = 60
attn_time = 7

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices
  
# Let's make one whole function 

def simulation_model(N_people, N_follows, wc, wnc, meme_init, total_memes, pn, pm, N, time_steps, attn_time):
    np.random.seed(50)
    G = nx.barabasi_albert_graph(N_people, N_follows)
    
    meme_init_dict = {'meme': [], 'type': [], 'weight': []}
    for i in range(1,meme_init+1):
        meme_init_dict['meme'].append(i)
        meme_init_dict['type'].append(random.choices(['C', 'NC'], weights = [wc, wnc])[0])
        if meme_init_dict['type'][i-1] == 'C':
            meme_init_dict['weight'].append(wc)
        else:
            meme_init_dict['weight'].append(wnc)
            
    meme_dict = {'meme': [], 'type': [], 'weight': []}
    for i in range(1,total_memes+1):
        meme_dict['meme'].append(i+50)
        meme_dict['type'].append(random.choices(['C', 'NC'], weights = [wc, wnc])[0])
        if meme_dict['type'][i-1] == 'C':
            meme_dict['weight'].append(wc)
        else:
            meme_dict['weight'].append(wnc)
            
    meme_data = {"agent": [], "meme": [], "type": [], "time": [], "state": [], "weight": [], "prob_share": []}
    screen_data = {'agent': [], 'sr_meme': [], 'sr_type': [], 'sr_weight': [], 'sr_follows': [], 'sr_time_cur': [], 'sr_time_meme': []}
    agent_posted = 0
    
    class Agent:
    # initialize internal variables
        def __init__(self, ID):
            self.ID = ID
            self.memory = {'meme' : [], 'type': [], 'weight': [], 'time' : []} # initialise one meme at t=0 in memory
            self.screen = {'meme' : [] , 'type': [], 'weight': [], 'time' : [], 'curr_time': [], 'follow_ID': []}
            self.current_time = 0
            self.follows = []
        
        def memory_init(self):
            m = random.choice(meme_init_dict['meme'])
            idx = meme_init_dict['meme'].index(m)
            self.memory['meme'].insert(0, m)
            self.memory['type'].insert(0, meme_init_dict['type'][idx])
            self.memory['time'].insert(0, 0)
            self.memory['weight'].insert(0, meme_init_dict['weight'][idx])
        
    
        def if_posted(self):
            self.posted = np.random.choice([True, False])
            return self.posted
        
        def forget_meme(self): # this would define breadth of user attention
            for i in range(len(self.memory['meme'])-1, 0, -1):
                if self.current_time - self.memory['time'][i] > attn_time:
                    del self.memory['meme'][i]
                    del self.memory['type'][i]
                    del self.memory['weight'][i]
                    del self.memory['time'][i] 
                
        def forget_screen(self): # this would define breadth of user attention
            for i in range(len(self.screen['meme'])-1, 0, -1):
                if self.current_time - self.screen['time'][i] > attn_time:
                    del self.screen['meme'][i]
                    del self.screen['type'][i]
                    del self.screen['weight'][i]
                    del self.screen['time'][i] 
                    del self.screen['curr_time'][i]
                    del self.screen['follow_ID'][i]
                    
    agents = [ Agent(ID) for ID in range(N_people) ]

    for edge in G.edges():
        i,j = edge
        agents[i].follows.append(j)
        agents[j].follows.append(i)
    
    
    # initalialise the memory for each agent
    for agent in agents:
        agent.memory_init()
    
    for time in range(1,time_steps+1):
        for agent in agents:
            agent.if_posted()
            simulated_user_post_new = random.uniform(0, 1) # randomly simulate new posts - pn
        # when we talk about memory or repost, we factor in the meme type to get probability
            simulated_user_post_memory = random.uniform(0, 1) # randomly simulate a post from memory - pm
            agent.current_time = time
        # populate user screen
            for i in range(len(agent.follows)):
                other = agents[agent.follows[i]]
                if pd.notna(other.memory["meme"][0]) == True:
                    agent.screen['meme'].append(other.memory['meme'][0])
                    agent.screen['type'].append(other.memory['type'][0])
                    agent.screen['weight'].append(other.memory['weight'][0])
                    agent.screen['time'].append(other.memory['time'][0])
                    agent.screen['follow_ID'].append(agent.follows[i])
                    agent.screen['curr_time'].append(time)
                else:
                    pass
            
        
        # calculate how many contentious memes were seen in last N time steps
            count_C = 0
            count_NC = 0
            t = time
            if t-N > 0:
                for i in range(t-N, t+1): # we want to access screen for last N steps (each will have its own meme list)
                    indices = find_indices(agent.screen['curr_time'], i)
                    if len(indices) != 0:
                        for index in indices:
                            if agent.screen['type'][index] == 'C':
                                count_C += 1
                            else:
                                count_NC += 1
         
            if count_C == 0:
                ps = 0
            else:
                ps = count_C/(count_C+count_NC)
        
        
        # New post
            if agent.posted == True and simulated_user_post_new <= pn:
            # append a new meme and time in memory
                m = random.choice(meme_dict['meme'])
                idx = meme_dict['meme'].index(m)
                agent.memory["meme"].insert(0, m)
                agent.memory["time"].insert(0, time)
                agent.memory['type'].insert(0, meme_dict['type'][idx])
                agent.memory['weight'].insert(0, meme_dict['weight'][idx])
            
                agent_posted = 1
            
        # Repost
            if agent.posted == True and simulated_user_post_new > pn and simulated_user_post_memory > 1-pm and len(agent.screen['meme']) != 0:
                chosen_meme_index = random.randrange(len(agent.screen['meme'])) # since we are randomly picking meme from screen, we just chose a random index for now
                if agent.screen['type'][chosen_meme_index] == 'C':
                    agent.memory["meme"].insert(0, agent.screen['meme'][chosen_meme_index])
                    agent.memory["time"].insert(0, time)
                    agent.memory["type"].insert(0, 'C')
                    agent.memory["weight"].insert(0,ps)
                
                else:
                    agent.memory["meme"].insert(0, agent.screen['meme'][chosen_meme_index])
                    agent.memory["time"].insert(0, time)
                    agent.memory["type"].insert(0, 'NC')
                    agent.memory["weight"].insert(0,pnc)
                
                agent_posted = 2
                
        # Memory
            if agent.posted == True and simulated_user_post_new > pn and simulated_user_post_memory <= pm and len(agent.memory['meme']) != 0 and sum(agent.memory['weight'])!=0:
                chosen_meme_index = random.choices(list(range(len(agent.memory["meme"]))), weights = agent.memory["weight"])[0]
                chosen_meme = agent.memory["meme"][chosen_meme_index]
                chosen_type = agent.memory["type"][chosen_meme_index]
            
                if chosen_type == 'C':
                    agent.memory["meme"].insert(0, chosen_meme)
                    agent.memory["time"].insert(0, time)
                    agent.memory["type"].insert(0, chosen_type)
                    agent.memory["weight"].insert(0,ps)
            
                else:
                    agent.memory["meme"].insert(0, chosen_meme)
                    agent.memory["time"].insert(0, time)
                    agent.memory["type"].insert(0, chosen_type)
                    agent.memory["weight"].insert(0,pnc)
                
                agent_posted = 3
                
            
            else:
                pass
                agent_posted = 0
                agent.memory["meme"].insert(0, np.NaN)
                agent.memory["time"].insert(0, time)
                agent.memory["type"].insert(0, np.NaN)
                agent.memory["weight"].insert(0, np.NaN)
        
            agent.forget_meme()
            agent.forget_screen()
            meme_data["agent"].append(agents.index(agent))
            meme_data["meme"].append(agent.memory["meme"][0])
            meme_data["time"].append(time)
            meme_data["type"].append(agent.memory["type"][0])
            meme_data["state"].append(agent_posted) 
            meme_data["weight"].append(agent.memory["weight"][0])
            meme_data["prob_share"].append(ps)
        
            for i in range(len(agent.screen['meme'])):
                screen_data['agent'].append(agents.index(agent))
                screen_data['sr_meme'].append(agent.screen['meme'][i])
                screen_data['sr_type'].append(agent.screen['type'][i])
                screen_data['sr_weight'].append(agent.screen['weight'][i])
                screen_data['sr_follows'].append(agent.screen['follow_ID'][i])
                screen_data['sr_time_cur'].append(time)
                screen_data['sr_time_meme'].append(agent.screen['time'][i])
                
    
    meme_data_df = pd.DataFrame(meme_data)
    screen_data_df = pd.DataFrame(screen_data)
    return meme_data_df
    
    
simulation_model_df = simulation_model(N_people, N_follows, wc, wnc, meme_init, total_memes, pn, pm, N, time_steps, attn_time)









