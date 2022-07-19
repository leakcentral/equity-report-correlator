import pandas as pd 
from openpyxl import workbook
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
import networkx.algorithms.community as nxcom
import igraph as ig
import random
from pyvis.network import Network
import matplotlib.cm as cm
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
from sklearn.metrics.cluster import adjusted_rand_score
import math
import community






def louvian(networkx_graph,notebook=True,output_filename='graph.html',show_buttons=True,only_physics_buttons=False,
                height=None,width=None,bgcolor=None,font_color=None,pyvis_options=None):
    """
    This function accepts a networkx graph object,
    converts it to a pyvis network object preserving its node and edge attributes,
    and both returns and saves a dynamic network visualization.
    Valid node attributes include:
        "size", "value", "title", "x", "y", "label", "color".
        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node)
    Valid edge attributes include:
        "arrowStrikethrough", "hidden", "physics", "title", "value", "width"
        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_edge)
    Args:
        networkx_graph: The graph to convert and display
        notebook: Display in Jupyter?
        output_filename: Where to save the converted network
        show_buttons: Show buttons in saved version of network?
        only_physics_buttons: Show only buttons controlling physics of network?
        height: height in px or %, e.g, "750px" or "100%
        width: width in px or %, e.g, "750px" or "100%
        bgcolor: background color, e.g., "black" or "#222222"
        font_color: font color,  e.g., "black" or "#222222"
        pyvis_options: provide pyvis-specific options (https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.options.Options.set)
    """
    

    
    colorFile = list(open('/Users/arnavp4/Desktop/Capstone Project/colors.txt'))

    color_list = []

    for color in colorFile:
        color_list.append(color.strip())


    partition_object = community.best_partition(G)
    values = [partition_object.get(node) for node in G.nodes()]
    color_list = color_list[0:len(set(values))]
    color_dict = pd.Series(color_list,
        index=np.arange(0,len(set(values)))).to_dict()




    for key, value in partition_object.items():
        partition_object[key] = color_dict[value]

    nx.set_node_attributes(G, partition_object, 'color')



    # make a pyvis network
    network_class_parameters = {"notebook": notebook, "height": height, "width": width, "bgcolor": bgcolor, "font_color": font_color}
    pyvis_graph = Network(**{parameter_name: parameter_value for parameter_name, parameter_value in network_class_parameters.items() if parameter_value})

    # for each node and its attributes in the networkx graph
    for node,node_attrs in networkx_graph.nodes(data=True):
        pyvis_graph.add_node(node,**node_attrs, shape = 'circle')

    # for each edge and its attributes in the networkx graph
    for source,target,edge_attrs in networkx_graph.edges(data=True):
        # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
        if not 'value' in edge_attrs and not 'width' in edge_attrs and 'weight' in edge_attrs:
            # place at key 'value' the weight of the edge
            edge_attrs['value']=edge_attrs['weight']
        # add the edge
        pyvis_graph.add_edge(source,target, value = 0.1)

    # turn buttons on
    if show_buttons:
        if only_physics_buttons:
            pyvis_graph.show_buttons(filter_=['physics'])
        else:
            pyvis_graph.show_buttons()

    # pyvis-specific options
    if pyvis_options:
        pyvis_graph.set_options(pyvis_options)

    # return and also save
    return pyvis_graph.show(output_filename)


def greedy(G):

    # Greedy Modularity Maximization algorithm
    d = list(greedy_modularity_communities(G))
    remove = []
    #print(c)
    # very good result only one(9 should be in first list) missed for 1
    partition = {}



    for i in range(len(d)):
        elements = list(d[i])
        #check length elements and add to list and delete those nodes
        if (len(elements) < 5):
            for x in elements:
                remove.append(x)
        for el in elements:
            partition[el] = i

    G.remove_nodes_from(remove)


    c = list(greedy_modularity_communities(G))
    partition = {}

    for i in range(len(c)):
        elements = list(c[i])
        for el in elements:
            partition[el] = i



    pos = nx.spring_layout(G)
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=20,
                        cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos, alpha=0.9, font_size = 8)
    plt.title('Greedy Modularity Maximization algorithm')
    plt.show()




    def plot_degree_dist(G):
        degrees = [G.degree(n) for n in G.nodes()]
        plt.hist(degrees)
        plt.show()

    #plot_degree_dist(G)




companies = list(open('/Users/arnavp4/Desktop/Capstone Project/companies'))

arr = []

for company in companies:
    arr.append(company.strip())


df = pd.read_csv('/Users/arnavp4/Desktop/Capstone Project/rawfinaldf.csv')

threshold = 0.3
df.where(df <= threshold, 1, inplace=True)
df.where(df >= threshold, 0, inplace=True)
A = df.to_numpy()
G = nx.from_numpy_matrix(A)
mapping = dict(zip(G, arr))
G = nx.relabel_nodes(G, mapping)




greedy(G)

louvian(G, height = '1000px', width = '1000px', 
            show_buttons=False,  
            output_filename='/Users/arnavp4/Desktop/Capstone Project/ereportgraph.html', notebook=False)







df2 = pd.read_csv('/Users/arnavp4/Desktop/Capstone Project/rawbetacorr.csv')

threshold = 0.95
df2.where(df2 <= threshold, 1, inplace=True)
df2.where(df2 >= threshold, 0, inplace=True)
B = df2.to_numpy()
H = nx.from_numpy_matrix(B)
mapping = dict(zip(H, arr))
H = nx.relabel_nodes(H, mapping)


greedy(H)

louvian(H, height = '1000px', width = '1000px', 
            show_buttons=False,  
            output_filename='/Users/arnavp4/Desktop/Capstone Project/betagraph.html', notebook=False)


