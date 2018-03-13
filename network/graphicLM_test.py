import os
import numpy as np
import pandas as pd
import networkx as nx
import graphicML

try:
    hd = 'H' + unichr(252) + 'sker D' + unichr(252)
    mh = 'Mot' + unichr(246) + 'rhead'
    mc = 'M' + unichr(246) + 'tley Cr' + unichr(252) + 'e'
    st = 'Sp' + unichr(305) + 'n' + unichr(776) + 'al Tap'
    q = 'Queensr' + unichr(255) + 'che'
    boc = 'Blue ' + unichr(214) + 'yster Cult'
    dt = 'Deatht' + unichr(246) + 'ngue'
except NameError:
    hd = 'H' + chr(252) + 'sker D' + chr(252)
    mh = 'Mot' + chr(246) + 'rhead'
    mc = 'M' + chr(246) + 'tley Cr' + chr(252) + 'e'
    st = 'Sp' + chr(305) + 'n' + chr(776) + 'al Tap'
    q = 'Queensr' + chr(255) + 'che'
    boc = 'Blue ' + chr(214) + 'yster Cult'
    dt = 'Deatht' + chr(246) + 'ngue'

G = nx.Graph()
G.add_edge(hd, mh)
G.add_edge(mc, st)
G.add_edge(boc, mc)
G.add_edge(boc, dt)
G.add_edge(st, dt)
G.add_edge(q, st)
G.add_edge(dt, mh)
G.add_edge(st, mh)

print('Graph was build.')

GA = graphicML.Attribute(G)

node = GA.node()
print(node.shape)

edge = GA.edge()
print(edge.shape)

attr = GA.graph_attributes()
print(attr.shape)
