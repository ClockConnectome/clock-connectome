def clock_neuron_connections(clock_df, direction):
    from neuprint import fetch_adjacencies
    
    if direction == 'out':
        # get outputs from clock neurons to anything else
        neuron_df, conn_df = fetch_adjacencies(clock_df['bodyId'], None, min_total_weight=1)
        column_to_group_on = 'bodyId_pre'
    if direction == 'in':
        # get inputs to clock neurons from anything else
        neuron_df, conn_df = fetch_adjacencies(None, clock_df['bodyId'], min_total_weight=1)
        column_to_group_on = 'bodyId_post'
    
    # consolidate since we don't care about separating connections between 2 neurons that happen in different ROIs.
    conns_df = conn_df.groupby(['bodyId_pre', 'bodyId_post'], as_index=False)['weight'].sum()
    
    # get total output synapse count for clock neurons
    syns_df = conns_df.groupby([column_to_group_on], as_index=False)['weight'].sum()
    syns_df = syns_df.rename(columns={"weight": f"num_{direction}_syns"})
    return conns_df, syns_df