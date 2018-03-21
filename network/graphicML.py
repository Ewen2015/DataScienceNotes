#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author: 	Ewen Wang
email: 		wang.enqun@outlook.com
license: 	Apache License 2.0
"""
import pandas as pd
import networkx as nx
import itertools 

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

def edge(graph):
	edge_attr = []
	edge_attr = pd.DataFrame(list(itertools.combinations(list(graph.nodes.keys()), r=2)), columns=['source', 'target'])
	edge_attr['shortest_path_length'] = edge_attr.apply(lambda x: shortest_path_len(graph, x[0], x[1]), axis=1)
	edge_attr['efficiency'] = edge_attr.apply(lambda x: nx.efficiency(graph, x[0], x[1]), axis=1)
	edge_attr['jaccard_coefficient'] = edge_attr.apply(lambda x: link_pred_generator(nx.jaccard_coefficient)(graph, x[0], x[1]), axis=1)
	edge_attr['resource_allocation_index'] = edge_attr.apply(lambda x: link_pred_generator(nx.resource_allocation_index)(graph, x[0], x[1]), axis=1)
	edge_attr['adamic_adar_index'] = edge_attr.apply(lambda x: link_pred_generator(nx.adamic_adar_index)(graph, x[0], x[1]), axis=1)
	edge_attr['preferential_attachment'] = edge_attr.apply(lambda x: link_pred_generator(nx.preferential_attachment)(graph, x[0], x[1]), axis=1)
	return edge_attr

class Attribute(object):

	def __init__(self, graph):
		self.graph = graph
		self.node_attr = pd.DataFrame()
		self.edge_attr = pd.DataFrame()
		self.graph_attr = pd.DataFrame()

	def node(self):
		degree_cent = pd.DataFrame(list(nx.degree_centrality(self.graph).items()), columns=['node', 'degree_centrality'])
		closenessCent = pd.DataFrame(list(nx.closeness_centrality(self.graph).items()), columns=['node', 'closeness_centrality'])
		betweennessCent = pd.DataFrame(list(nx.betweenness_centrality(self.graph).items()), columns=['node', 'betweenness_centrality'])
		pagerank = pd.DataFrame(list(nx.pagerank(self.graph).items()), columns=['node', 'pagerank'])

		self.node_attr = degree_cent
		self.node_attr['closeness_centrality'] = closenessCent['closeness_centrality']
		self.node_attr['betweenness_centrality'] = betweennessCent['betweenness_centrality']
		self.node_attr['pagerank'] = pagerank['pagerank']
		return self.node_attr

	def edge(self):
		self.edge_attr = edge(self.graph)
		return self.edge_attr

	def graph_attributes(self):
		self.node_attr = self.node()
		self.edge_attr = self.edge()
		self.graph_attr = self.edge_attr.merge(self.node_attr, how='left', left_on='source', right_on='node').merge(self.node_attr, how='left', left_on='target', right_on='node')	
		self.graph_attr = self.graph_attr.drop(['node_x', 'node_y'], axis=1)
		return self.graph_attr

class NodePairs(object):
	"""docstring for NodePairs"""
	def __init__(self, data, source, target):
		super(NodePairs, self).__init__()
		self.data = data
		self.source = source
		self.target = target

	
		
