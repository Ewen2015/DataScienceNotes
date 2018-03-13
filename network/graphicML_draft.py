import os
import numpy as np
import pandas as pd
import networkx as nx
import itertools 


def node_attr(graph, k=6):

	node_attr = []
	degree_cent = pd.DataFrame(list(nx.degree_centrality(graph).items()), columns=['node', 'degree_centrality'])
	closenessCent = pd.DataFrame(list(nx.closeness_centrality(graph).items()), columns=['node', 'closeness_centrality'])
	betweennessCent = pd.DataFrame(list(nx.betweenness_centrality(graph, k).items()), columns=['node', 'betweenness_centrality'])
	pagerank = pd.DataFrame(list(nx.pagerank(graph).items()), columns=['node', 'pagerank'])

	node_attr = degree_cent
	node_attr['closeness_centrality'] = closenessCent['closeness_centrality']
	node_attr['betweenness_centrality'] = betweennessCent['betweenness_centrality']
	node_attr['pagerank'] = pagerank['pagerank']

	return node_attr

def shortest_path_len(graph, source, target):
	if nx.has_path(graph, source, target):
		return nx.shortest_path_length(graph, source, target)
	else:
		return None

def link_pred_generator(function):
	def link_pred(graph, source, target):
		for u, v, p in function(graph, [(source, target)]):
			return p
	return link_pred

def edge_attr(graph):

	edge_attr = []

	edge_attr = pd.DataFrame(list(itertools.combinations(list(graph.nodes.keys()), r=2)), columns=['source', 'target'])
	edge_attr['shortest_path_length'] = edge_attr.apply(lambda x: shortest_path_len(graph, x[0], x[1]), axis=1)
	edge_attr['efficiency'] = edge_attr.apply(lambda x: nx.efficiency(graph, x[0], x[1]), axis=1)

	edge_attr['jaccard_coefficient'] = edge_attr.apply(lambda x: link_pred_generator(nx.jaccard_coefficient)(graph, x[0], x[1]), axis=1)
	edge_attr['resource_allocation_index'] = edge_attr.apply(lambda x: link_pred_generator(nx.resource_allocation_index)(graph, x[0], x[1]), axis=1)
	edge_attr['adamic_adar_index'] = edge_attr.apply(lambda x: link_pred_generator(nx.adamic_adar_index)(graph, x[0], x[1]), axis=1)
	edge_attr['preferential_attachment'] = edge_attr.apply(lambda x: link_pred_generator(nx.preferential_attachment)(graph, x[0], x[1]), axis=1)

	return edge_attr

def graph_attr(node_attr, edge_attr):
	merged = edge_attr.merge(node_attr, how='left', left_on='source', right_on='node').merge(node_attr, how='left', left_on='target', right_on='node')
	return merged







