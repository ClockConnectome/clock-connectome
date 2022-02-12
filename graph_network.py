import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

def clock_type_network(conn_df, dot_name = None):
    """
    Generates type collapsed version of intra clock connections with networkx

    :param conn_df: Any connections dataframe that includes all relevant connections, weight cutoff already done
    :param dot_name: name of exported dot file
    :return: (DiGraph) of connections between clock neurons
    """
    conn_df = conn_df.groupby(['instance_pre', 'instance_post'], as_index=False).sum()
    conn_df = conn_df.replace("_R", "", regex=True)[['instance_pre', 'instance_post', 'weight']]

    G = nx.from_pandas_edgelist(conn_df, 'instance_pre', 'instance_post', edge_attr='weight', create_using=nx.DiGraph())
    
    import math

    weights = list(nx.get_edge_attributes(G, 'weight').values())
    weights = [math.log(w) for w in weights]
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
    nx.draw_circular(G, with_labels=True, ax=ax, connectionstyle='arc3, rad = 0.1', width=list(weights), node_color=values, edge_color=e_colors)
    nx.draw_networkx_edge_labels(G, pos, label_pos=.8, edge_labels=nx.get_edge_attributes(G, 'weight'))

    # Parallel edge weights overlap on networkx, export to dot file
    if dot_name is not None:
        write_dot(G, dot_name + '.svg')

    return G

def neuron_graph(conn_df, dot_name = None):
    conn_df = conn_df[['instance_pre', 'instance_post', 'weight']]
    G = nx.from_pandas_edgelist(conn_df, 'instance_pre', 'instance_post', edge_attr='weight', create_using=nx.DiGraph())

    import math
    weights = list(nx.get_edge_attributes(G, 'weight').values())
    weights = [math.log(w) for w in weights]

    #TODO: consider a different workaround for coloring 5th s-LNv
    val_map = {'sLNv': '#9D3434',
               'DN1a': '#C597D4',
               'DN1pA': '#3963A1',
               'DN1pB': '#3963A1',
               'LNd': '#E1B464',
               'LPN': '#4A7A0F',
               '5th sLN': '#D86E6E'}
    values = [val_map.get(node[0:-1]) for node in G.nodes()]
    e_colors = [val_map.get(u[0:-1]) for u, v in G.edges()]

    fig = plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1', width=list(weights), node_color=values,
            edge_color=e_colors, font_color="whitesmoke", node_size=2000)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

    #Parallel edge weights overlap on networkx, export to dot file
    if dot_name is not None:
        write_dot(G, dot_name + '.svg')