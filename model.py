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
                #print(agent.screen['curr_time'].index(i))
                indices = find_indices(agent.screen['curr_time'], i)
                #print(indices)
                if len(indices) != 0:
                    for index in indices:
                        #print('index:', index)
                        #print('type:', agent.screen['type'][index])
                        # or agent.screen['type'][index] == ['C']
                        if agent.screen['type'][index] == 'C':
                            count_C += 1
                            #print(count_C)
                        else:
                            count_NC += 1
         
        if count_C == 0:
            ps = 0
            #print(ps)
        else:
            ps = count_C/(count_C+count_NC)
            #print(ps)# prob of sharing for contentious meme
        
        
        
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
            #chosen_meme_index = random.randrange(len(agent.screen['meme']))
            #norm = [float(i)/sum(agent.memory['weight']) for i in agent.memory['weight']]
            #print(sum(agent.memory["weight"]))
            #print(agent.memory["meme"])
            #print(agent.memory["weight"])
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
            #print('Agent did not post')
            agent_posted = 0
            agent.memory["meme"].insert(0, np.NaN)
            agent.memory["time"].insert(0, time)
            agent.memory["type"].insert(0, np.NaN)
            agent.memory["weight"].insert(0, np.NaN)
        
        #print(agent.memory["weight"])
        
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
        #print(time) 
                
          
meme_data_df = pd.DataFrame(meme_data)
