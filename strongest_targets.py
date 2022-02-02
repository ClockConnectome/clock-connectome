def get_strong_shared_targs(IDs, shared_num):
  from neuprint import fetch_simple_connections

  test = fetch_simple_connections(IDs, None, min_weight=10)
  test['shared'] = 1
      
  test = test.groupby(['bodyId_post'], as_index=False)['weight','shared'].sum()
  test = test.sort_values(by=['weight'], ascending=False)
  test = test.loc[test['shared']==shared_num]

  return test

def get_input_output_conns(IDs, strength, direction):
    """
    Retrieves data for candidate neuron inputs or outputs and returns them sorted by weight
    :param candidate_IDs: the bodyIds of the neurons of interest
    :param strength: (int) minimum connection strength
    :param direction: (string) specified connection direction to run:
        'in' for inputs to clock neurons from anything else, 
        'out' for outputs from clock neurons to anything else.
    :return:
    """
    from neuprint import fetch_simple_connections
    if direction == 'in':
        candidate_conns = fetch_simple_connections(None, IDs, min_weight=strength)
        candidate_conns = candidate_conns[['bodyId_post','instance_post','bodyId_pre','instance_pre','weight']]
        candidate_conns = candidate_conns.sort_values(by=['bodyId_post','weight'], ascending = False)
    if direction == 'out':
        candidate_conns = fetch_simple_connections(IDs, None, min_weight=strength)
        candidate_conns = candidate_conns[['bodyId_pre','instance_pre','bodyId_post','instance_post','weight']]
        candidate_conns = candidate_conns.sort_values(by=['bodyId_pre','weight'], ascending = False)
    return candidate_conns