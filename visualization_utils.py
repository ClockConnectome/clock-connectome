from supervenn import supervenn
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib.pyplot import figure
import pandas as pd

def supervenn_comps(conn_df, clock_df, group, direction, bodyIds = None, weighted = False):
    """
    Using the supervenn library, generates and saves out .png and .svg formats of the overlap similarity diagrams

    :param conn_df: Any connections dataframe that includes all relevant connections, weight cutoff already done
    :param clock_df: Clock dataframe
    :param group: Name of clock group featured in figure OR some other identifying name for labels
    :param direction: Out for connections of clock neurons to other neurons, in for connections of clock neurons from other neurons
    :param bodyIds: (optional) provide bodyIds of neurons in figure
    :param weighted: Whether generated figure visually represent weights of each connection
    :return:
    """

    if direction == "out":
        clock_col = 'bodyId_pre'
        partner_col = 'bodyId_post'
    elif direction == "in":
        clock_col = 'bodyId_post'
        partner_col = 'bodyId_pre'

    if bodyIds is None:
        bodyIds = clock_df.loc[clock_df['type'] == group, 'bodyId']

    sets = []
    if weighted:
        for id in bodyIds:
            df = conn_df.loc[conn_df[clock_col] == id, [partner_col, 'weight']]
            list_s = df.apply(lambda row: [str(row['bodyId_post']) + '_' + str(x) for x in range(row['weight'])],
                              axis=1).tolist()
            sets.append(set([item for sublist in list_s for item in sublist]))
    else:
        for s in bodyIds:
            sets.append(set(conn_df.loc[conn_df[clock_col] == s, partner_col]))

    fig, ax = plt.subplots(figsize=(10, 8))
    labels = clock_df.loc[clock_df['bodyId'].isin(bodyIds), 'labels'].reset_index()['labels']
    supervenn(sets, labels, side_plots='right', chunks_ordering='minimize gaps')

    if direction == "out":
        plt.xlabel('# of target neurons')
    elif direction == "in":
        plt.xlabel('# of input neurons')

    plt.ylabel(group + 's')
    plt.title('overlap of ' + group + ' targets')
    fig.savefig('vectorized_' + group + '_targets.png')
    fig.savefig('vectorized_' + group + '_targets.svg', format='svg')

def jaccard_vis(conn_df, clock_df, clockIds, otherBodyIds = None):
    """
    Calculates jaccard values and visualizes as a heatmap

    :param conn_df: Any connections dataframe that includes all relevant connections, weight cutoff already done
    :param clock_df: Clock dataframe
    :param clockIds: The body ids of clock neurons in this jaccard visualization
    :param otherBodyIds: Any other body ids, clock not included
    :return:
    """

    clockIds = pd.Series(clockIds)
    clockNames = clock_df.loc[clock_df['bodyId'].isin(clockIds)]['labels']
    allNames = clockNames.append(otherBodyIds)

    if otherBodyIds is None:
        allIds = clockIds
        otherBodyIds = allIds
        otherNames = clockNames
    else:
        allIds = clockIds.append(pd.Series(otherBodyIds))
        otherNames = pd.Series(otherBodyIds)

    jaccard_AB = np.zeros((len(otherBodyIds), len(allIds)))
    i_ind = 0
    j_ind = 0

    for i in otherBodyIds:
        setA = set(conn_df.loc[conn_df['bodyId_pre'] == i, 'bodyId_post'])

        for j in allIds:
            setB = set(conn_df.loc[conn_df['bodyId_pre'] == j, 'bodyId_post'])
            setAuB = setA.union(setB)
            setAiB = setA.intersection(setB)
            jaccard_AB[i_ind, j_ind] = len(setAiB) / len(setAuB)
            j_ind += 1

        i_ind += 1
        j_ind = 0

    #mask = np.zeros_like(jaccard_AB)
    #mask[np.triu_indices_from(mask)] = True (add mask = mask to heatmap if this is used)

    figure(figsize=(len(allIds), len(otherBodyIds)), dpi=80)
    sb.heatmap(jaccard_AB, vmin=0, vmax=1, annot=True, fmt='.2f', xticklabels=allNames,
               yticklabels=otherNames, cmap=sb.light_palette("seagreen", as_cmap=True),
               cbar_kws={'label': 'Jaccard index'})

    #plt.title("Strong and medium outputs")
    #plt.savefig("jac_LN_outputs.svg")