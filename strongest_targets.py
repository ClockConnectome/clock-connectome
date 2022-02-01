def get_strong_shared_targs(IDs):
    """
    Gets strong shared targets of specified bodyIds for the neuron type
    :param IDs: list of bodyIds
    :return:
    """
    from neuprint import fetch_simple_connections
    
    test = fetch_simple_connections(IDs, None)
    test['shared'] = 0
    post_IDs = set(test['bodyId_post'])

    for p in post_IDs:
        pre_list = test.loc[test['bodyId_post']==p, 'bodyId_pre']
        if len(pre_list) > 3:
            test.loc[test['bodyId_post']==p, 'shared'] = 1
      
    test = test.groupby(['bodyId_post'], as_index=False)['weight'].sum()
    test = test.sort_values(by=['weight'], ascending=False)

    return test

def strongest_shared_targets(candidate_IDs, direction):
    """
    Retrieves data for candidate neuron inputs or outputs and returns them sorted by weight
    :param candidate_IDs: the bodyIds of the neurons of interest
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else, 
        'out' for outputs from clock neurons to anything else.
    :return:
    """
    from neuprint import fetch_simple_connections
    if direction == 'in':
        candidate_conns = fetch_simple_connections(None, candidate_IDs)
        candidate_conns = candidate_conns[['bodyId_post','bodyId_pre','instance_pre','weight']]
        candidate_conns = candidate_conns.sort_values(by=['bodyId_post','weight'], ascending = False)
    if direction == 'out':
        candidate_conns = fetch_simple_connections(candidate_IDs, None)
        candidate_conns = candidate_conns[['bodyId_pre','bodyId_post','instance_post','weight']]
        candidate_conns = candidate_conns.sort_values(by=['bodyId_pre','weight'], ascending = False)
    return candidate_conns