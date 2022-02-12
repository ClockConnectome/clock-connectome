import pandas as pd

def clock_neuron_connections(clock_df, direction, min_weight=1):
    """
    Gets input/output connections of clock neurons as well as connections between clock neurons.

    :param clock_df: the dataframe generated by getClock()
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else, 
        'out' for outputs from clock neurons to anything else,
        'intra_clock' for connections between clock neurons.
    :param min_weight: minimum weight in one direction required between two neurons to be included
    :return: (Dataframe) of clock connections in requested direction
    """
    from neuprint import fetch_adjacencies, merge_neuron_properties
    
    if direction == 'out':
        # get outputs from clock neurons to anything else
        neuron_df, conn_df = fetch_adjacencies(clock_df['bodyId'], None, min_total_weight=min_weight)
    if direction == 'in':
        # get inputs to clock neurons from anything else
        neuron_df, conn_df = fetch_adjacencies(None, clock_df['bodyId'], min_total_weight=min_weight)
    if direction == 'intra_clock':
        #getting the connections between clock neurons
        neuron_df, conn_df = fetch_adjacencies(clock_df['bodyId'], clock_df['bodyId'], min_total_weight=min_weight)
    
    # consolidate since we don't care about separating connections between 2 neurons that happen in different ROIs.
    conn_df = conn_df.groupby(['bodyId_pre', 'bodyId_post'], as_index=False)['weight'].sum()

    # merge on instance information
    neuron_df = neuron_df.merge(clock_df[['bodyId', 'labels']], how='left')
    neuron_df.loc[neuron_df['labels'].isnull(), 'labels'] = neuron_df['type']
    neuron_df['instance'] = neuron_df['labels']
    conn_df = merge_neuron_properties(neuron_df, conn_df, properties=['instance'])

    return conn_df

def synapse_count(conns_df, direction, intra_clock=False):
    """
    Gets total input or output synapse count for clock neurons.

    :param conns_df: the table of connections generated by clock_neuron_connections()
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else, 
        'out' for outputs from clock neurons to anything else.
    :param intra_clock: default False. Set to True for synapse count between clock neurons.
        If set to True, adds the string 'clock' to the output column name for differentiating purposes.
    :return: (Dataframe) of total synapse counts of each clock neuron
    """
    clock = ''

    if direction == 'out':
        column_to_group_on = 'bodyId_pre'
    if direction == 'in':
        column_to_group_on = 'bodyId_post'
    if intra_clock:
        clock = 'clock_'

    syns_df = conns_df.groupby([column_to_group_on], as_index=False)['weight'].sum()
    syns_df = syns_df.rename(columns={"weight": f"num_{clock}{direction}_syns",column_to_group_on:"bodyId"})
    
    return syns_df

def synaptic_partner_numbers(conns_df, direction, intra_clock=False):
    """
    Get number of pre or postsynaptic partners of the clock neurons using value_counts of the post or presynaptic bodyIds
    
    :param conns_df: the table of connections generated by clock_neuron_connections()
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else, 
        'out' for outputs from clock neurons to anything else.
    :param intra_clock: default False. Set to True for synapse count between clock neurons.
        If set to True, adds the string 'clock' to the output column name for differentiating purposes.
    :return: (Dataframe) of number of different partners of clock neurons
    """ 
    clock = ''
    if direction == 'out':
        column_to_group_on = 'bodyId_pre'
        pre_or_post = 'post'
    if direction == 'in':
        column_to_group_on = 'bodyId_post'
        pre_or_post = 'pre'
    if intra_clock:
        clock = 'clock_'

    partners_df = conns_df[column_to_group_on].value_counts().to_frame().reset_index()
    partners_df = partners_df.rename(columns={"index":"bodyId", column_to_group_on:f"num_{clock}{pre_or_post}syn_partners"})

    return partners_df

def ranked_lists(clock_df, conns_sort, direction):
    """
    Generates a dataframe with each 'type' of pre or postsynaptic neurons ranked by weight
    
    :param clock_df: clock dataframe
    :param conns_sort: dataframe of connection information sorted from highest to lowest number of synaptic connections for each neuron
    :param direction: string determining if it's looking at synaptic inputs (in) or targets (out)
    :return: (Dataframe) of ranked list of connections for each neuron in the clock network
    """

    tables = []
    #looking at one particular type at a time
    types = clock_df['type'].unique()
    for group in types:
        #these are all the body Ids of that type
        IDs = clock_df[clock_df['type']==group]['bodyId']
        #looking at one neuron at a time
        for ID in IDs:
            #takes only the rows where the presynaptic neuron is that neuron
            if direction == 'post':
                sub_conns = conns_sort[conns_sort["bodyId_pre"] == ID]
                sub_conns = sub_conns[['bodyId_post', 'instance_post', 'weight']]
            #takes only the rows where the postsynaptic neuron is that neuron
            if direction == 'pre':
                sub_conns = conns_sort[conns_sort["bodyId_post"] == ID]
                sub_conns = sub_conns[['bodyId_pre', 'instance_pre', 'weight']]
            sub_conns.reset_index(drop=True, inplace=True)
            #adds on that information onto post_tables
            tables.append(sub_conns)

    all_grouped = pd.concat(tables, axis = 1) # this concat does funky things to the bodyIds
    # please include clock neuron info along top of the DF before returning
    return all_grouped

def intra_conns(clock_df, type_or_phase):
    """
    Retrieve body ids within each type/phase then retrieve only those rows where both in and out are of the same type.
    :param clock_df: clock dataframe
    :param type_or_phase: (string) whether to call the function on each type or each phase.
    :return: (Dataframe) of the intra-clock connections
    """
    from neuprint import fetch_adjacencies
    
    intra_conns = []
    
    if type_or_phase == 'type':
        unique = clock_df.type.unique()
        class_or_me = 'class'
    if type_or_phase == 'phase':
        unique = clock_df.phase.unique()
        class_or_me = 'me'

    for t in unique:
        ids = clock_df[clock_df[type_or_phase] == t]['bodyId'].tolist()
        neuron_df, conn_df = fetch_adjacencies(ids, ids)
        out_df = conn_df.groupby(['bodyId_pre'], as_index=False)['weight'].sum() 
        in_df = conn_df.groupby(['bodyId_post'], as_index=False)['weight'].sum()
        conns = pd.merge(in_df, out_df.set_index('bodyId_pre'), left_on = 'bodyId_post', right_index = True)
        conns = conns.rename(columns={"bodyId_post":"bodyId","weight_x":f"{class_or_me}_syn_in","weight_y":f"{class_or_me}_syn_out"})
        intra_conns.append(conns)

    conns = pd.concat(intra_conns)
    if type_or_phase == 'phase':
        me_ids = clock_df[clock_df['phase'] != '']['bodyId'].tolist()
        conns = conns[conns['bodyId'].isin(me_ids)]
    return conns

def group_summary(conn_summary_df, clock_df, type_or_phase):
    """
    :param conn_summary_df: connection summary table
    :param clock_df: clock dataframe
    :type_or_phase: (string) whether to group by type or phase
    :return:
    """
    #Merge type back on for easy grouping
    conn_group_df = conn_summary_df.merge(clock_df[['bodyId', type_or_phase]])

    #Use group_by to get summations
    conn_group_df = conn_group_df.groupby([type_or_phase]).sum()
    del conn_group_df['bodyId']

    # Subtract out class synapses and reorder
    class_synapses = conn_group_df['class_syn_in']
    conn_group_df = conn_group_df.sub(class_synapses, axis = 0)
    conn_group_df['class_syn_in'] = class_synapses

    if type_or_phase == 'type':
        groups = ['l-LNv', 's-LNv', '5th s-LNv', 'LNd', 'LPN', 'DN1a', 'DN1pA', 'DN1pB']
        conn_group_df = conn_group_df.reindex(groups)

    # reorder columns
    conn_group_df = conn_group_df[['num_in_syns', 'num_presyn_partners', 'num_out_syns', 'num_postsyn_partners', 'class_syn_in', 'num_clock_in_syns', 'num_clock_out_syns']]
    return conn_group_df

def strong_shared_connections(body_ids, direction, shared_num):
    """
    Gets strong shared targets (body id and total shared weight)
    :param body_ids: candidate IDs
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else, 
        'out' for outputs from clock neurons to anything else.
    :param shared_num: (int) minimum shared target number to look at
    :return: (Dataframe) of shared targets and the total shared weight
    """
    from neuprint import fetch_simple_connections

    if direction == 'out':
        conns_df = fetch_simple_connections(body_ids, None, min_weight=10)
        conns_df['shared'] = 1
        conns_df = conns_df.fillna(value='None')
        conns_df = conns_df.groupby(['bodyId_post', 'instance_post'], as_index=False)['weight', 'shared'].sum()
    if direction == 'in':
        conns_df = fetch_simple_connections(None, body_ids, min_weight=10)
        conns_df['shared'] = 1
        conns_df = conns_df.fillna(value='None')
        conns_df = conns_df.groupby(['bodyId_pre', 'instance_pre'], as_index=False)['weight', 'shared'].sum()

    conns_df = conns_df.sort_values(by=['weight'], ascending=False)
    shared_targets = conns_df.loc[test['shared'] >= shared_num]

    return shared_targets


def get_input_output_conns(body_ids, strength, direction):
    """
    Retrieves data for candidate neuron inputs or outputs and returns them sorted by weight
    :param body_ids: the body IDs of the neurons of interest
    :param strength: (int) minimum connection strength
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else, 
        'out' for outputs from clock neurons to anything else.
    :return: (Dataframe) of connections for candidate neurons
    """
    from neuprint import fetch_simple_connections
    if direction == 'in':
        candidate_conns = fetch_simple_connections(None, body_ids, min_weight=strength)
        candidate_conns = candidate_conns[['bodyId_post', 'instance_post', 'bodyId_pre', 'instance_pre', 'weight']]
        candidate_conns = candidate_conns.sort_values(by=['bodyId_post', 'weight'], ascending=False)
    if direction == 'out':
        candidate_conns = fetch_simple_connections(body_ids, None, min_weight=strength)
        candidate_conns = candidate_conns[['bodyId_pre', 'instance_pre', 'bodyId_post', 'instance_post', 'weight']]
        candidate_conns = candidate_conns.sort_values(by=['bodyId_pre', 'weight'], ascending=False)
    return candidate_conns
