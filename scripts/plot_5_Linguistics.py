# This script produces plot 5 in the Linguistics paper, a plot that visualizes the Vneo values of five German word formation suffixes.

# import necessary libraries
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import re

vneo_tum = pd.read_csv("TUM_vneo_global_100000.csv", sep = ",", index_col = 0)
vneo_bar = pd.read_csv("BAR_vneo_global_100000.csv", sep = ",", index_col = 0)
vneo_ieren = pd.read_csv("IEREN_vneo_global_100000.csv", sep = ",", index_col = 0)
vneo_isch = pd.read_csv("ISCH_vneo_global_100000.csv", sep = ",", index_col = 0)
vneo_nis = pd.read_csv("NIS_vneo_global_100000.csv", sep = ",", index_col = 0)

decs = range(1700,1910,10)

# this function draws the areas into which a given amount (conf) data fall.
# It takes as an argument a dataframe with a given number of simulations (df), x-values (x), a boundary (as a fraction of 1) (conf), a colour (col), and a plot (plot_x).
# the idea is to sort the actual values of the simulations for each decade;
# then we determine which values serve as lower and upper boundaries;
# and then to plot an area with these boundaries.
def conf_int(df, x, conf, col, plot_x):
    nr_sim = df.shape[0]

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

def figure_env(ax, name):
    ax.set_xlim(1700,1900)
    ax.set_xticks(decs[::2])
    ax.set_xticklabels(decs[::2], rotation=45)
    ax.set_title(name, fontweight = "bold")
    ax.set_ylim(0,300)
    ax.grid()


# plot 5
fig = plt.figure(figsize = (12,9))

ax1 = fig.add_subplot(321)
ax1.plot(list(vneo_tum),vneo_tum.mean(axis = 0, skipna =  True).values, linewidth = 0.7, color = "black")
conf_int(vneo_tum, decs, 0.99, 'grey', ax1)
conf_int(vneo_tum, decs, 0.95,'dimgrey', ax1)
figure_env(ax1, "-tum")

ax2 = fig.add_subplot(322)
ax2.plot(list(vneo_bar),vneo_bar.mean(axis = 0, skipna =  True).values, linewidth = 0.7, color = "black")
conf_int(vneo_bar, decs, 0.99, 'grey', ax2)
conf_int(vneo_bar, decs, 0.95,'dimgrey', ax2)
figure_env(ax2, "-bar")

ax3 = fig.add_subplot(323)
ax3.plot(list(vneo_ieren),vneo_ieren.mean(axis = 0, skipna =  True).values, linewidth = 0.7, color = "black")
conf_int(vneo_ieren, decs, 0.99, 'grey', ax3)
conf_int(vneo_ieren, decs, 0.95,'dimgrey', ax3)
figure_env(ax3, "-ieren")

ax4 = fig.add_subplot(324)
ax4.plot(list(vneo_isch),vneo_isch.mean(axis = 0, skipna =  True).values, linewidth = 0.7, color = "black")
conf_int(vneo_isch, decs, 0.99, 'grey', ax4)
conf_int(vneo_isch, decs, 0.95,'dimgrey', ax4)
figure_env(ax4, "-isch")

ax5 = fig.add_subplot(325)
ax5.plot(list(vneo_nis),vneo_nis.mean(axis = 0, skipna =  True).values, linewidth = 0.7, color = "black")
conf_int(vneo_nis, decs, 0.99, 'grey', ax5)
conf_int(vneo_nis, decs, 0.95,'dimgrey', ax5)
figure_env(ax5, "-nis")

fig.text(0.5, 0.005, 'decades', ha='center', size = 14)
fig.text(0.005, 0.5, '#new types', va='center', rotation='vertical', size = 14)

fig.tight_layout(pad = 2)
fig.savefig('plot_5_Linguistics.png', dpi=800)
