import os
from gremthon import Gremthon
example_graph_son = '{}/doctors-consumers-graph.json'.format(os.environ['TEST_DRIVE_DIR'])
g = Gremthon(rexster.getGraph("graph"))
count = g.V.count()
if count == 0:
    g.input_graph(example_graph_son)
