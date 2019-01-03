# This script produces plot 3 in the Linguistics paper, a plot that visualizes the changes in types and tokens in each decade.

# import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

decs = range(1490,1910,10)

# this function returns the number of types and tokens for each decade
def types(df):
    df_result = pd.DataFrame(index = decs, columns = ["types"])
    df_result = df_result.fillna(0)
    for dec in decs:
        df_result.loc[dec,"types"] = len(set(df[df["Dekade"] <= dec]["Lemma"]))
    return(df_result)

def tokens(df):
    df_result = pd.DataFrame(index = decs, columns = ["tokens"])
    df_result = df_result.fillna(0)
    for dec in decs:
        df_result.loc[dec,"tokens"] = sum(df[df["Dekade"] <= dec]["Freq"])
    return(df_result)

def delta(df, dta):
    df_result = pd.DataFrame(index = decs, columns = ("dtokens" , "dtypes"))
    df_result = df_result.fillna(0)
    for dec in range(1490,1900,10):
        df_result.loc[dec,"dtokens"] = dta.loc[dec+10, "tokens"] - dta.loc[dec, "tokens"]
        df_result.loc[dec,"dtypes"] = df.loc[dec+10, "types"] - df.loc[dec, "types"]
    df_result["delta"]=df_result["dtypes"]/df_result["dtokens"]
    df_result["dec"] = decs
    df_result = df_result.fillna(0)
    return(df_result)

def delta_plot(df):
    df_result = pd.DataFrame(index = range(1490,1905,5), columns = ("tokens" , "delta"))
    df_result = df_result.fillna(0)
    for dec in range(1495,1905,5):
        df_result.loc[dec,"tokens"] = sum(df[df["dec"] <= dec]["dtokens"])
        df_result.loc[dec+5,"delta"] = df[df["dec"] == int(dec/10)*10]["delta"].values
    return(df_result)

def paint_centuries(ax):
    # add vertical lines indicating centuries
    ax.axvline(x=tokens_dta.tokens[1600], color="grey")
    ax.axvline(x=tokens_dta.tokens[1700], color="grey")
    ax.axvline(x=tokens_dta.tokens[1800], color="grey")
    ax.axvline(x=tokens_dta.tokens[1900], color="grey")
    # add century labels
    ax.text(tokens_dta.tokens[1600]+10000, 0.000045, "1600", color="grey", size=12)
    ax.text(tokens_dta.tokens[1700]+10000, 0.000045, "1700", color="grey", size=12)
    ax.text(tokens_dta.tokens[1800]+10000, 0.000045, "1800", color="grey", size=12)
    ax.text(tokens_dta.tokens[1900]-10000, 0.000045, "1900", color="grey", horizontalalignment='right', size=12)
    ax.set_xticks(range(0,175000000,25000000))
    ax.set_xticklabels(range(0,175,25), size = 14)
    ax.set_ylim(0,0.00005)
    ax.grid(axis = "y", linestyle="--")


# read the necessary files:
texts_dta  = pd.read_csv('texts_dta.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
bar  = pd.read_csv('bar_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
isch  = pd.read_csv('isch_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
nis  = pd.read_csv('nis_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
tum  = pd.read_csv('tum_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
ieren  = pd.read_csv('ieren_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count

tokens_dta = tokens(texts_dta)

bar_tt = types(bar)
bar_delta = delta(bar_tt, tokens_dta)
bar_delta_plot = delta_plot(bar_delta)

isch_tt = types(isch)
isch_delta = delta(isch_tt, tokens_dta)
isch_delta_plot = delta_plot(isch_delta)

nis_tt = types(nis)
nis_delta = delta(nis_tt, tokens_dta)
nis_delta_plot = delta_plot(nis_delta)

ieren_tt = types(ieren)
ieren_delta = delta(ieren_tt, tokens_dta)
ieren_delta_plot = delta_plot(ieren_delta)

tum_tt = types(tum)
tum_delta = delta(tum_tt, tokens_dta)
tum_delta_plot = delta_plot(tum_delta)

# plot 3
fig = plt.figure(figsize = (12,9))

ax1 = fig.add_subplot(321)
paint_centuries(ax1)
ax1.plot(bar_delta_plot["tokens"], bar_delta_plot["delta"], '-', color = "black")
ax1.set_title("-bar", fontweight = "bold")

ax2 = fig.add_subplot(322)
paint_centuries(ax2)
ax2.plot(isch_delta_plot["tokens"], isch_delta_plot["delta"], '-', color = "black")
ax2.set_title("-isch", fontweight = "bold")

ax3 = fig.add_subplot(323)
paint_centuries(ax3)
ax3.plot(nis_delta_plot["tokens"], nis_delta_plot["delta"], '-', color = "black")
ax3.set_title("-nis", fontweight = "bold")

ax4 = fig.add_subplot(324)
paint_centuries(ax4)
ax4.plot(ieren_delta_plot["tokens"], ieren_delta_plot["delta"], '-', color = "black")
ax4.set_title("-ieren", fontweight = "bold")

ax5 = fig.add_subplot(325)
paint_centuries(ax5)
ax5.plot(tum_delta_plot["tokens"], tum_delta_plot["delta"], '-', color = "black")
ax5.set_title("-tum", fontweight = "bold")

fig.text(0.5, 0.005, 'tokens (in millions)', ha='center', size = 14)
fig.text(0.005, 0.5, 'Δtypes/Δtokens', va='center', rotation='vertical', size = 14)
# add legend
#ax1.legend(loc=2, bbox_to_anchor = (0.05,0.95), prop={'size': 14})

fig.tight_layout(pad = 2)
fig.savefig('plot_3_Linguistics.png', dpi=800)
