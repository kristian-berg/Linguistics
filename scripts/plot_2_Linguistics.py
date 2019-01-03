# This script produces plot 2 in the Linguistics paper, a lineplot with tokens on the x-axis
# and types on the y-axis for the different word formation patterns.

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


# read the necessary files:
texts_dta  = pd.read_csv('texts_dta.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
bar  = pd.read_csv('bar_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
isch  = pd.read_csv('isch_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
nis  = pd.read_csv('nis_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
tum  = pd.read_csv('tum_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
ieren  = pd.read_csv('ieren_neu.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
bar_tt = types(bar)
isch_tt = types(isch)
nis_tt = types(nis)
tum_tt = types(tum)
ieren_tt = types(ieren)
tokens_dta = tokens(texts_dta)


# plot 2
fig = plt.figure(figsize = (12,6))
ax1 = fig.add_subplot(111)

# add vertical lines indicating centuries
ax1.axvline(x=tokens_dta.tokens[1600], color="grey")
ax1.axvline(x=tokens_dta.tokens[1700], color="grey")
ax1.axvline(x=tokens_dta.tokens[1800], color="grey")
ax1.axvline(x=tokens_dta.tokens[1900], color="grey")

# add grid
ax1.grid(axis = "y", linestyle="--")

# add century labels
ax1.text(tokens_dta.tokens[1600]+10000, 5050, "1600", color="grey", size=12)
ax1.text(tokens_dta.tokens[1700]+10000, 5050, "1700", color="grey", size=12)
ax1.text(tokens_dta.tokens[1800]+10000, 5050, "1800", color="grey", size=12)
ax1.text(tokens_dta.tokens[1900]-10000, 5050, "1900", color="grey", horizontalalignment='right', size=12)

# add growth lines
ax1.plot(tokens_dta.tokens, isch_tt.types, '-o', color = "black", label="-isch")
ax1.plot(tokens_dta.tokens, ieren_tt.types, '-o', color = "grey", label="-ieren")
ax1.plot(tokens_dta.tokens, bar_tt.types, '-.o', color = "grey", label="-bar")
ax1.plot(tokens_dta.tokens, tum_tt.types, '--o', color = "grey", label="-tum")
ax1.plot(tokens_dta.tokens, nis_tt.types, '--o', color = "black", label="-nis")


# modify xticks, set labels
ax1.set_xticks(range(0,175000000,25000000))
ax1.set_xticklabels(range(0,175,25), size = 14)
ax1.set_xlabel("#tokens (in millions)", size=14)
ax1.set_ylabel("#types", size=14)


# add legend
ax1.legend(loc=2, bbox_to_anchor = (0.05,0.95), prop={'size': 14}, handlelength = 3)

fig.tight_layout(pad = 2)
fig.savefig('plot_2_Linguistics.png', dpi=800)
