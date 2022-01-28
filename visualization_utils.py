from supervenn import supervenn
import matplotlib.pyplot as plt

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
            sets.append(set(conn_df.loc[conn_df['bodyId_pre'] == s, 'bodyId_post']))

    fig, ax = plt.subplots(figsize=(10, 8))
    labels = clock_df.loc[clock_df['bodyId'].isin(bodyIds), 'seqInstance'].reset_index()['seqInstance']
    supervenn(sets, labels, side_plots='right', chunks_ordering='minimize gaps')

    if direction == "out":
        plt.xlabel('# of target neurons')
    elif direction == "in":
        plt.xlabel('# of input neurons')

    plt.ylabel(group + 's')
    plt.title('overlap of ' + group + ' targets')
    fig.savefig('vectorized_' + group + '_targets.png')
    fig.savefig('vectorized_' + group + '_targets.svg', format='svg')

def jaccard_vis(bodyIds):
    pass