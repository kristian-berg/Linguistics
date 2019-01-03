# This script produces plot 10 in the Linguistics paper, a plot that visualizes the changes in types and tokens in each decade.

# import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

decs = range(1700,1910,10)


def figure_env(ax, name):
    ax.grid()
    ax.set_title(name, fontweight = "bold")
    ax.set_xticks(decs[::2])
    ax.set_xticklabels(decs[::2], rotation=45)
    #ax.set_ylim(0,1)

def conf_int(df, x, conf, col, plot_x):
    nr_sim = df.shape[0]
    print(nr_sim)

    conf_max = int(round(nr_sim * conf -1))  # upper boundary. example: p = 0.9, nr_sim =1000. conf_max = 899. In an ascending list of values for each decade, the 899th of 1,000 values is the upper boundary (for p = 0.9)
    conf_min = nr_sim - conf_max -1  # lower boundary. example: nr_sim =1000. conf_min = 1000 - 899 -1 = 100

    df =  df.transpose()
    df.values.sort() # sort the values
    line = np.empty([2, len(df)], dtype= float) # set up an empty array that contains values for two lines.

    inx = 0 #set up counter to specify row number
    for row in df.iterrows():
        if conf_max <= 0: # if conf_max is equal to or below zero, there is no boundary
            line[0,inx] = None
            line[1,inx] = None
        else:   # if conf_max is above zero, the line values (upper and lower boundaries) are simply the conf_max-th and conf_min-th value of all simulation values for each decade
            df_nan = df.iloc[inx,:].dropna()
            if len(df_nan) == 0:
                line[0,inx] = None
                line[1,inx] = None
            else:
                if df_nan.shape[0] == nr_sim:
                    line[0,inx] = df.iloc[inx,conf_min]
                    line[1,inx] = df.iloc[inx,conf_max]
                else:
                    conf_min_nan = int(round((df_nan.shape[0] * conf_min)/nr_sim))
                    conf_max_nan = int(round((df_nan.shape[0] * conf_max)/nr_sim))
                    line[0,inx] = df_nan.iloc[conf_min_nan]
                    line[1,inx] = df_nan.iloc[conf_max_nan]
        inx +=1
    plot_x.fill_between(x,  line[0,:], line[1,:], facecolor=col, alpha='0.5') # fill the area that is enclosed by the lines


# read the necessary files:
bar_vneo  = pd.read_csv('bar_vneo_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
isch_vneo  = pd.read_csv('isch_vneo_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
nis_vneo  = pd.read_csv('nis_vneo_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
tum_vneo  = pd.read_csv('tum_vneo_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
ieren_vneo  = pd.read_csv('ieren_vneo_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count

bar_hap  = pd.read_csv('bar_hapax_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
isch_hap  = pd.read_csv('isch_hapax_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
nis_hap  = pd.read_csv('nis_hapax_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
tum_hap  = pd.read_csv('tum_hapax_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count
ieren_hap  = pd.read_csv('ieren_hapax_global_100000.csv', sep= ',',index_col=0) # this file contains a line for each text in the corpus, together with the respective decade and the token count

# plot 11
fig = plt.figure(figsize = (12,9))

ax1 = fig.add_subplot(321)
ax1.plot(list(bar_hap), bar_hap.mean(axis = 0, skipna =  True).values, color = "grey")
ax1.plot(list(bar_vneo), bar_vneo.mean(axis = 0, skipna =  True).values, color = "black")
figure_env(ax1, "-bar")
print("bar OK")

ax2 = fig.add_subplot(322)
ax2.plot(list(isch_hap), isch_hap.mean(axis = 0, skipna =  True).values, color = "grey")
ax2.plot(list(isch_vneo), isch_vneo.mean(axis = 0, skipna =  True).values, color = "black")
figure_env(ax2, "-isch")
print("isch OK")

ax3 = fig.add_subplot(323)
ax3.plot(list(nis_hap), nis_hap.mean(axis = 0, skipna =  True).values, color = "grey")
ax3.plot(list(nis_vneo), nis_vneo.mean(axis = 0, skipna =  True).values, color = "black")
figure_env(ax3, "-nis")
print("nis OK")

ax4 = fig.add_subplot(324)
ax4.plot(list(ieren_hap), ieren_hap.mean(axis = 0, skipna =  True).values, color = "grey")
ax4.plot(list(ieren_vneo), ieren_vneo.mean(axis = 0, skipna =  True).values, color = "black")
figure_env(ax4, "-ieren")
print("ieren OK")

ax5 = fig.add_subplot(325)
ax5.plot(list(tum_hap), tum_hap.mean(axis = 0, skipna =  True).values, color = "grey", label = "hapax legomena")
ax5.plot(list(tum_vneo), tum_vneo.mean(axis = 0, skipna =  True).values, color = "black", label = "new words")
figure_env(ax5, "-tum")
ax5.legend(bbox_to_anchor = [1.1 , 0.5], loc='center left', prop={'size': 14}, frameon=False)
print("tum OK")



# add legend
#ax1.legend(loc=2, bbox_to_anchor = (0.05,0.95), prop={'size': 14})

fig.tight_layout(pad = 2)
fig.savefig('plot_10_Linguistics.png', dpi=800)
