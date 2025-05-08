import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 import data and assign to df variable
df = pd.read_csv("medical_examination.csv")

# 2 Add an overweight column to the data
bmi = df['weight'] / ((df['height'] / 100)**2)
overweight_values = []
for value in bmi:
    if value > 25:
        overweight_values.append(1)
    else:
        overweight_values.append(0)

df['overweight'] = overweight_values

# 3 Normalize cholesterol and gluc data by making 0 always good and 1 always bad

cholesterol_normalized = []
for value in df['cholesterol']:
    if value == 1:
        cholesterol_normalized.append(0)
    else:
        cholesterol_normalized.append(1)
df['cholesterol'] = cholesterol_normalized

gluc_normalized = []
for value in df['gluc']:
    if value == 1:
        gluc_normalized.append(0)
    else:
        gluc_normalized.append(1)
df['gluc'] = gluc_normalized

# 4 Draw the Categorical Plot
def draw_cat_plot():
    # 5 Create a DataFrame for the cat plot using pd.melt 
    df_cat = pd.melt(df, id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6 Group and reformat the data in df_cat to split it by cardio
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    
    # 7 Convert the data into long format and create a char
    cat_plot = sns.catplot(
        data = df_cat,
        kind='bar',
        x = 'variable',
        y = 'total',
        col='cardio',
        hue='value'
    )

    # 8 Get the figure for the output and store it in the fig variable
    fig = cat_plot.figure

    # 9
    fig.savefig('catplot.png')
    return fig

# 10 Draw the Heat Map
def draw_heat_map():
    # 11 Clean the data 
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & 
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) & 
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12 Calculate the correlation matrix
    corr = df_heat.corr()

    # 13 Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))

    # 14 Set up the matplotlib figure.
    fig, ax = plt.subplots()

    # 15 Plot the correlation matrix
    sns.heatmap(
        corr,  
        vmin = -0.12,
        vmax = 0.26,
        mask = mask,
        annot = True, 
        annot_kws = {'size':5, 'weight':'bold'},
        fmt ='.1f',
        center = 0,
        linewidths=0.5, 
        cbar_kws= {'shrink': 0.6}
    )

    ax.tick_params(labelsize=6)

    # 16
    fig.savefig('heatmap.png')
    return fig
