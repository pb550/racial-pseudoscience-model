# Agent class definition

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
