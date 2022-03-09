from supervenn import supervenn
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib.pyplot import figure
import pandas as pd

def supervenn_comps(conn_df, clock_df, body_ids, direction, file_name, weighted = False, annot_width = 1):
    """
    Using the supervenn library, generates and saves out .png and .svg formats of the overlap similarity diagrams

    :param conn_df: Any connections dataframe that includes all relevant connections, weight cutoff already done
    :param clock_df: Clock dataframe
    :param body_ids: BodyIds of neurons in figure
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else,
        'out' for outputs from clock neurons to anything else.
    :param file_name: Name of neuron group to be used for file naming
    :param weighted: Whether generated figure visually represent weights of each connection
    :return:
    """

    if direction == "out":
        clock_col = 'bodyId_pre'
        partner_col = 'bodyId_post'
    elif direction == "in":
        clock_col = 'bodyId_post'
        partner_col = 'bodyId_pre'

    sets = []

    # Generate sets of inputs/targets for each neuron, adding indexes to create multiples if weighted = True
    if weighted:
        for id in body_ids:
            df = conn_df.loc[conn_df[clock_col] == id, [partner_col, 'weight']]
            list_s = df.apply(lambda row: [str(row['bodyId_post']) + '_' + str(x) for x in range(row['weight'])],
                              axis=1).tolist()
            sets.append(set([item for sublist in list_s for item in sublist]))
    else:
        for s in body_ids:
            sets.append(set(conn_df.loc[conn_df[clock_col] == s, partner_col]))

    # Generate figure and label
    fig, ax = plt.subplots(figsize=(10, 8))
    labels = clock_df.loc[clock_df['bodyId'].isin(body_ids), 'labels'].reset_index()['labels']
    supervenn(sets, labels, side_plots='right', chunks_ordering='minimize gaps', min_width_for_annotation = annot_width)

    if direction == "out":
        d = 'target'
    elif direction == "in":
        d = 'input'

    plt.xlabel('# of ' + d + ' neurons')
    plt.ylabel(file_name + 's')
    plt.title('overlap of ' + file_name + ' ' + d + 's')
    fig.savefig('vectorized_' + file_name + '_' + d + 's.png')
    fig.savefig('vectorized_' + file_name + '_' + d + 's.svg', format='svg')

def jaccard_vis(conn_df, clock_df, clock_ids, direction, other_body_ids = None, diag_mask=False):
    """
    Calculates jaccard values and visualizes as a heatmap

    :param conn_df: Any connections dataframe that includes all relevant connections, weight cutoff already done
    :param clock_df: Clock dataframe
    :param clock_ids: The body ids of clock neurons in this jaccard visualization
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else,
        'out' for outputs from clock neurons to anything else.
    :param other_body_ids: Any other body ids, clock not included
    :return: (Matrix) of jaccard similarity values
    """

    # Retrieve descriptive names
    clock_ids = pd.Series(clock_ids)
    clock_names = clock_df.loc[clock_df['bodyId'].isin(clock_ids)]['labels']
    all_names = clock_names.append(other_body_ids)

    # If no second set of body ids is provide, assume the first set of ids is compared to itself
    if other_body_ids is None:
        all_ids = clock_ids
        other_body_ids = all_ids
        other_names = clock_names
    else:
        all_ids = clock_ids.append(pd.Series(other_body_ids))
        other_names = pd.Series(other_body_ids)

    # Supply correct columns for data retrieval
    if direction == "out":
        clock_col = 'bodyId_pre'
        partner_col = 'bodyId_post'
    elif direction == "in":
        clock_col = 'bodyId_post'
        partner_col = 'bodyId_pre'

    # Create and fill in matrix of jaccard values between ids
    jaccard_AB = np.zeros((len(other_body_ids), len(all_ids)))
    i_ind = 0
    j_ind = 0

    for i in other_body_ids:
        setA = set(conn_df.loc[conn_df[clock_col] == i, partner_col])

        for j in all_ids:
            setB = set(conn_df.loc[conn_df[clock_col] == j, partner_col])
            setAuB = setA.union(setB)
            setAiB = setA.intersection(setB)
            jaccard_AB[i_ind, j_ind] = len(setAiB) / len(setAuB)
            j_ind += 1

        i_ind += 1
        j_ind = 0

    # Jaccard figure        
    fig = figure(figsize=(len(all_ids), len(other_body_ids)), dpi=80)
    if diag_mask==True:
        mask = np.zeros_like(jaccard_AB)
        mask[np.triu_indices_from(mask)] = True
        mask[np.diag_indices_from(mask)] = False
        mask[jaccard_AB==0] = True
        sb.heatmap(jaccard_AB, mask=mask, vmin=0, vmax=1, annot=True, fmt='.2f', xticklabels=all_names,
               yticklabels=other_names, cmap=sb.light_palette("seagreen", as_cmap=True),
               cbar_kws={'label': 'Jaccard index'})
    else:
        sb.heatmap(jaccard_AB, vmin=0, vmax=1, annot=True, fmt='.2f', xticklabels=all_names,
               yticklabels=other_names, cmap=sb.light_palette("seagreen", as_cmap=True),
               cbar_kws={'label': 'Jaccard index'})
            
    return(jaccard_AB, fig)


def jaccard_simple(x_ids, y_ids, direction, diag_mask=False):
    """
    Calculates jaccard values and visualizes as a heatmap

    :param x_ids: The body ids of neurons to be shown on the x axis in this jaccard visualization
    :param y_ids: The body ids of neurons to be shown on the y axis in this jaccard visualization
    :param direction: (string) specified connection direction to run:
        'in' for inputs to neurons from anything else,
        'out' for outputs from neurons to anything else.
    :return: (Matrix) of jaccard similarity values
    """

    all_ids = pd.concat([x_ids, y_ids])
    
    # Supply correct columns for data retrieval and fetch connections df
    if direction == "out":
        clock_col = 'bodyId_pre'
        partner_col = 'bodyId_post'
        conn_df = fetch_simple_connections(all_ids, None, min_weight=3)
    elif direction == "in":
        clock_col = 'bodyId_post'
        partner_col = 'bodyId_pre'
        conn_df = fetch_simple_connections(None, all_ids, min_weight=3)
        
    # Create and fill in matrix of jaccard values between ids
    jaccard_AB = np.zeros((len(y_ids), len(x_ids)))
    i_ind = 0
    j_ind = 0

    for i in y_ids:
        setA = set(conn_df.loc[conn_df[clock_col] == i, partner_col])

        for j in x_ids:
            setB = set(conn_df.loc[conn_df[clock_col] == j, partner_col])
            setAuB = setA.union(setB)
            setAiB = setA.intersection(setB)
            jaccard_AB[i_ind, j_ind] = len(setAiB) / len(setAuB)
            j_ind += 1

        i_ind += 1
        j_ind = 0

    # Jaccard figure        
    fig = figure(figsize=(len(x_ids), len(y_ids)), dpi=80)
    if diag_mask==True:
        mask = np.zeros_like(jaccard_AB)
        mask[np.triu_indices_from(mask)] = True
        mask[np.diag_indices_from(mask)] = False
        mask[jaccard_AB==0] = True
        sb.heatmap(jaccard_AB, mask=mask, vmin=0, vmax=1, annot=True, fmt='.2f', xticklabels=x_ids,
               yticklabels=y_ids, cmap=sb.light_palette("seagreen", as_cmap=True),
               cbar_kws={'label': 'Jaccard index'})
    else:
        sb.heatmap(jaccard_AB, vmin=0, vmax=1, annot=True, fmt='.2f', xticklabels=x_ids,
               yticklabels=y_ids, cmap=sb.light_palette("seagreen", as_cmap=True),
               cbar_kws={'label': 'Jaccard index'})
            
    return(jaccard_AB, fig)