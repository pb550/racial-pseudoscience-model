def simulation_graphs(df):
    # Graph number 1
    # Percentage of C vs NC memes
    ax1 = sns.displot(c_vs_nc(df), x="meme_type_ratio", hue="type")
    ax1.set(title='Frequency Distribution Meme Count - C vs NC', xlabel= 'Ratio of C or NC Memes', ylabel = 'Count')
    plt.savefig('Graphs/C_vs_NC1.png')
    plt.close()
    
    # Graph number 2
    # Total memes posted at each time step
    ax2 = sns.scatterplot(x="time", y="meme_count", data=memes_posted(df), hue="type")
    ax2.set(title='Meme Count at Each Time Step', xlabel='Time', ylabel='Meme Count')
    plt.savefig('Graphs/Meme_Count_Each_Time.png')
    plt.close()
    
    # Graph 3
    # Avg System entropy vs time
    ax3 = sns.scatterplot(x="time", y="avg_sys_entropy", data=sys_ent(df), hue="type")
    ax3.set(title='Average System Entropy vs Time', xlabel='Time', ylabel='System Entropy')
    plt.savefig('Graphs/Average_System_Entropy.png')
    plt.close()
    
    # Grah 4 
    # Attention span of users - determines how long the meme stays in user's memory
    # Breadth of User attention
    ax4 = sns.displot(attn_span(df), x="breadth_attn", hue="type")
    ax4.set(title='Probability Distribution of Breath of Attention', xlabel='Breadth of User Attention', ylabel='PDF')
    plt.savefig('Graphs/Breadth_of_Attention.png')
    plt.close()
    
    # Graph 5
    # Meme Lifetime
    ax5 = sns.displot(meme_lift(df), x="time_list", kind="kde", hue="type", fill=True)
    ax5.fig.set_figwidth(8.27)
    ax5.fig.set_figheight(5.5)
    ax5.set(title='Frequency Distribution Meme Lifetime', xlabel= 'Meme Lifetime', ylabel = 'Count')
    plt.savefig('Graphs/Meme_Lifetime.png')
    plt.close()
    
    # Graph 6
    # User Activity
    ax6 = sns.displot(user_act(df), x="activity", hue="type", kind="kde", fill=True)
    ax6.set(title='Probability Distribution of User Activity', xlabel='User Activity', ylabel='PDF')
    plt.savefig('Graphs/User_Activity.png')
    plt.close()
    
    # Graph 7
    # Meme Popularity
    ax7 = sns.displot(meme_pop(df), x="popularity", hue="type", kind="kde", fill=True)
    ax7.set(title='Probability Distribution of Meme Popularity', xlabel='Meme Popularity', ylabel='PDF')
    plt.savefig('Graphs/Meme_Popularity.png')
    plt.close()

    
