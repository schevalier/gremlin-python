from gremthon import Gremthon

#Java imports
from com.tinkerpop.blueprints.impls.tg import TinkerGraphFactory

graph = TinkerGraphFactory.createTinkerGraph()
g = Gremthon(graph)


def test_gremthon_repr():
    """
        Verify repr of a gremthon wrapped graph
    """
    assert str(g) == 'tinkergraph[vertices:6 edges:6]'

