#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author: 	Ewen Wang
email: 		wang.enqun@outlook.com
license: 	Apache License 2.0
"""
import os
import numpy as np
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


class Attribute(object):
	"""docstring for Attribute"""
	def __init__(self, graph):
		self.graph = graph
		self.node_attr = pd.DataFrame()
		self.edge_attr = pd.DataFrame()
		self.graph_attr = pd.DataFrame()

	def node_attr(self, k=6):
		degree_cent = pd.DataFrame(list(nx.degree_centrality(self.graph).items()), columns=['node', 'degree_centrality'])
		closenessCent = pd.DataFrame(list(nx.closeness_centrality(self.graph).items()), columns=['node', 'closeness_centrality'])
		betweennessCent = pd.DataFrame(list(nx.betweenness_centrality(self.graph, k).items()), columns=['node', 'betweenness_centrality'])
		pagerank = pd.DataFrame(list(nx.pagerank(self.graph).items()), columns=['node', 'pagerank'])

		self.node_attr = degree_cent
		self.node_attr['closeness_centrality'] = closenessCent['closeness_centrality']
		self.node_attr['betweenness_centrality'] = betweennessCent['betweenness_centrality']
		self.node_attr['pagerank'] = pagerank['pagerank']
		return self.node_attr

	def edge_attr(self):
		self.edge_attr = pd.DataFrame(list(itertools.combinations(list(self.graph.nodes.keys()), r=2)), columns=['source', 'target'])
		self.edge_attr['shortest_path_length'] = self.edge_attr.apply(lambda x: shortest_path_len(self.graph, x[0], x[1]), axis=1)
		self.edge_attr['efficiency'] = self.edge_attr.apply(lambda x: nx.efficiency(self.graph, x[0], x[1]), axis=1)

		self.edge_attr['jaccard_coefficient'] = self.edge_attr.apply(lambda x: link_pred_generator(nx.jaccard_coefficient)(self.graph, x[0], x[1]), axis=1)
		self.edge_attr['resource_allocation_index'] = self.edge_attr.apply(lambda x: link_pred_generator(nx.resource_allocation_index)(self.graph, x[0], x[1]), axis=1)
		self.edge_attr['adamic_adar_index'] = self.edge_attr.apply(lambda x: link_pred_generator(nx.adamic_adar_index)(self.graph, x[0], x[1]), axis=1)
		self.edge_attr['preferential_attachment'] = self.edge_attr.apply(lambda x: link_pred_generator(nx.preferential_attachment)(self.graph, x[0], x[1]), axis=1)
		return self.edge_attr

	def graph_attr(self):
		self.graph_attr = self.edge_attr.merge(self.node_attr, how='left', left_on='source', right_on='node').merge(self.node_attr, how='left', left_on='target', right_on='node')	
		return self.graph_attr
