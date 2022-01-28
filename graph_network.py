import matplotlib.pyplot as plt
import networkx as nx

def clock_type_network(conn_df):
    """
    Generates type collapsed version of intra clock connections with networkx

    :param conn_df: Any connections dataframe that includes all relevant connections, weight cutoff already done
    :return:
    """
    conn_df = conn_df.groupby(['type_pre', 'type_post'], as_index=False).sum()
    conn_df = conn_df.groupby(['type_pre', 'type_post'], as_index=False).sum()[['type_pre', 'type_post', 'weight']]

    G = nx.from_pandas_edgelist(conn_df, 'type_pre', 'type_post', edge_attr='weight', create_using=nx.DiGraph())
    fig, ax = plt.subplots(figsize=(10, 10))
    pos = nx.circular_layout(G)
    nx.draw_circular(G, with_labels=True, ax=ax, connectionstyle='arc3, rad = 0.1')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    
    '''import math

    weights = list(nx.get_edge_attributes(G, 'weight').values())
    # weights = [min(w, 10) for w in weights]
    weights = [math.ceil(math.log(w)) for w in weights]
    val_map = {'s-LNv': '#9D3434',
               'DN1a': '#C597D4',
               'DN1pA': '#3963A1',
               'DN1pB': '#3963A1',
               'LNd': '#E1B464',
               'LPN': '#4A7A0F',
               '5th s-LNv': '#D86E6E'}
    values = [val_map.get(node) for node in G.nodes()]
    e_colors = [val_map.get(u) for u, v in G.edges()]

    fig, ax = plt.subplots(figsize=(10, 10))
    pos = nx.circular_layout(G)
    # nx.draw_circular(G, with_labels=True, ax = ax, connectionstyle='arc3, rad = 0.1', width = list(weights), node_color = values, edge_color = e_colors)
    nx.draw_circular(G, with_labels=True, ax=ax, connectionstyle='arc3, rad = 0.1', node_color=values,
                     edge_color=e_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))'''

    return G