# Graph number 1
    # Percentage of C vs NC memes
def c_vs_nc(df):    
    meme_data_c_vs_nc = df
    meme_data_c_vs_nc = meme_data_c_vs_nc.groupby(['agent', 'type'])['meme'].size().reset_index(name = 'meme_count')
    meme_data_c_vs_nc['meme_type_ratio'] = meme_data_c_vs_nc['meme_count']/meme_data_c_vs_nc.groupby(["agent"])["meme_count"].transform("sum")
    
    return meme_data_c_vs_nc
    
# Graph number 2
    # Total memes posted at each time step
def memes_posted(df):
    top_meme = df
    top_meme = top_meme.groupby(['time', 'type', 'meme']).size().reset_index(name = 'agent_count')
    c_vs_nc = top_meme.groupby(['time', 'type']).size().reset_index(name = 'meme_count')
    
    return c_vs_nc
  
 # Graph 3
    # Avg System entropy vs time
def sys_ent(df):
    meme_data_se = df
    meme_data_se = meme_data_se.groupby(['time', 'meme', 'type']).size().reset_index(name = 'meme_count')
    meme_data_se['sys_entropy'] =  meme_data_se['meme_count']/meme_data_se.groupby(["time"])["meme_count"].transform("sum")
    meme_data_se['sys_entropy'] = meme_data_se['sys_entropy']*(-1)*(np.log(meme_data_se['sys_entropy']))
    meme_data_se = meme_data_se.groupby(['time', 'type'])['sys_entropy'].mean().reset_index(name = 'avg_sys_entropy')
    
    return meme_data_se
  
 # Grah 4 
    # Attention span of users - determines how long the meme stays in user's memory
    # Breadth of User attention
def attn_span(df):    
    meme_data_ba = df
    meme_data_ba = meme_data_ba.groupby(['agent', 'meme', 'type']).size().reset_index(name = 'meme_count')
    meme_data_ba['breadth_attn'] = meme_data_ba['meme_count']/meme_data_ba.groupby(["agent"])["meme_count"].transform("sum")
    meme_data_ba['breadth_attn'] = meme_data_ba['breadth_attn']*(-1)*(np.log(meme_data_ba['breadth_attn']))
    
    return meme_data_ba

# Graph 5
# Meme Lifetime

# function to find out maximum consecutive time units for each meme
def max_Consec_Time(my_lis, len_my_lis):
    # Insert all the elements of the list in an onordered set
    S = set() 
    
    for i in range(len_my_lis):
        S.add(my_lis[i])
    
    consec_time = 0;
    for i in range(len_my_lis):
        
        #if current element is the starting element of the sequence
        if S.__contains__(my_lis[i]):
            # then check for next element in the sequence
            j = my_lis[i]
            
            # increment the value of array element and repeat search in the set
            while(S.__contains__(j)):
                j += 1
                
            # Update optimal length if this length is more. To get the length as it is incremented one by one
            consec_time = max(consec_time, j - my_lis[i])
            
    return consec_time
  
# Graph 5
# Meme Lifetime
def meme_lift(df):
    meme_lifetime = df
    meme_lifetime = meme_lifetime.groupby(['meme', 'type'])['time'].apply(list).reset_index(name='time_list')
    meme_lifetime['time_list'] = meme_lifetime['time_list'].apply(lambda x: max_Consec_Time(x, len(x)))
    
    return meme_lifetime
  
# Graph 6
    # User Activity
def user_act(df):
    user_activity = df
    user_activity = user_activity.groupby(['agent', 'type', 'time']).size().reset_index(name = 'meme_count')
    user_activity = user_activity.groupby(['agent', 'type']).meme_count.sum().reset_index(name = 'total_memes')
    user_activity['activity'] = user_activity['total_memes']/time_steps
    
    return user_activity
  
# Graph 7
    # Meme Popularity
def meme_pop(df):
    meme_popularity = df.groupby(['meme', 'type', 'time']).size().reset_index(name = 'agent_count')
    meme_popularity = meme_popularity.groupby(['meme', 'type']).agent_count.sum().reset_index(name = 'popularity')
    
    return meme_popularity
