from gremthon import Gremthon
import os
import tempfile

#Java imports
from com.tinkerpop.blueprints import Direction, Vertex, Edge
from com.tinkerpop.blueprints.impls.tg import TinkerGraphFactory
from com.thinkaurelius.titan.core import TitanFactory
from com.thinkaurelius.titan.core import Order
from com.thinkaurelius.titan.core import Multiplicity
from com.thinkaurelius.titan.core.attribute import Decimal
from com.thinkaurelius.titan.graphdb.types.vertices import PropertyKeyVertex
from com.thinkaurelius.titan.graphdb.types import StandardPropertyKeyMaker
from com.thinkaurelius.titan.graphdb.types.vertices import EdgeLabelVertex
from com.thinkaurelius.titan.graphdb.types import StandardEdgeLabelMaker
from com.thinkaurelius.titan.graphdb.types import VertexLabelVertex
from com.thinkaurelius.titan.graphdb.types import StandardVertexLabelMaker
from com.thinkaurelius.titan.core import Cardinality
from java.lang import Double, String, Integer



graph = TinkerGraphFactory.createTinkerGraph()
titan_graph = TitanFactory.build().set('storage.backend','inmemory').open()

g = Gremthon(graph)
tg = Gremthon(titan_graph)


def test_gremthon_repr():
    """
        Verify repr of a gremthon wrapped graph
    """
    assert str(g) == 'tinkergraph[vertices:6 edges:6]'


def test_gremthon_titan_repr():
    """
        Verify repr of a gremthon wrapped titan graph
    """
    assert str(tg) == 'titangraph[inmemory:[127.0.0.1]]'


def test_no_management_system():
    assert g.management_system is None


def test_management_system():
    assert tg.management_system is not None


def test_make_vertex_label():
    ms = tg.management_system
    vl = ms.make_vertex_label('person')
    assert vl is not None
    assert isinstance(vl, VertexLabelVertex) is True
    assert vl.name == 'person'

    vlm = ms.make_vertex_label('label2', auto_make=False)
    assert vlm is not None
    assert isinstance(vlm, StandardVertexLabelMaker) is True
    assert vlm.getName() == 'label2'

    ms.commit()

    v1 = tg.add_vertex(vertex_label='label1', first_name='Jane', last_name='Doe')
    tg.commit()
    assert v1.label == 'label1'
    assert v1.first_name == 'Jane'
    assert v1.last_name == 'Doe'

    assert set(tg.V.id()) == {v1.id}


def test_vertex_labels():
    assert tg.management_system.vertex_labels()


def test_make_edge_label():
    ms = tg.management_system
    el = ms.make_edge_label('edge1')
    assert el is not None
    assert isinstance(el, EdgeLabelVertex) is True
    assert el.name == 'edge1'

    elm = ms.make_edge_label('edge2', auto_make=False)
    assert elm is not None
    assert isinstance(elm, StandardEdgeLabelMaker) is True
    assert elm.name == 'edge2'

    el = ms.make_edge_label('many2one_edge', multiplicity=Multiplicity.MANY2ONE)
    assert el is not None
    assert isinstance(el, EdgeLabelVertex) is True
    assert el.name == 'many2one_edge'

    ms.commit()

    assert tg.management_system.contains_relation_type('edge1') is True


def test_make_property_key():
    ms = tg.management_system
    ms.default_cardinality = Cardinality.SINGLE
    pk = ms.make_property_key('property1')
    assert pk is not None
    assert isinstance(pk, PropertyKeyVertex) is True
    assert pk.name == 'property1'
    assert pk.getCardinality() == Cardinality.SINGLE
    assert pk.getDataType() == String

    ms.commit()
    assert tg.management_system.contains_relation_type('property1') is True
    assert tg.management_system.relation_type('property1') == pk

    pk2 = tg.management_system.make_property_key('property2', cardinality=Cardinality.LIST)
    assert pk2 is not None
    assert isinstance(pk2, PropertyKeyVertex) is True
    assert pk2.name == 'property2'
    assert pk2.getCardinality() == Cardinality.LIST
    assert pk2.getDataType() == String

    pk3 = tg.management_system.make_property_key('property3', cardinality=Cardinality.SINGLE, data_type=Double)
    assert pk3 is not None
    assert isinstance(pk3, PropertyKeyVertex) is True
    assert pk3.name == 'property3'
    assert pk3.getCardinality() == Cardinality.SINGLE
    assert pk3.getDataType() == Double

    pk4 = tg.management_system.make_property_key('property4', auto_make=False)
    assert pk4 is not None
    assert isinstance(pk4, StandardPropertyKeyMaker) is True
    assert pk4.name == 'property4'


def test_build_index():
    ms = tg.management_system
    name = ms.make_property_key('name')
    age = ms.make_property_key('age', data_type=Integer)
    ms.build_index('by-name', Vertex, keys=[name])
    ms.build_index('by-name-and-age', Vertex, keys=[name, age])
    ms.commit()

    v = tg.add_vertex(name='hercules', age=30)
    tg.commit()
    assert v.name == 'hercules'
    assert v.age == 30

    assert len(set(tg.V.has('name','hercules'))) == 1
    assert len(set(tg.V.has('age',30).has('name','hercules'))) == 1
    assert len(set(tg.V.has('age',30))) == 1

    # TODO: is there an easy way to verify with an 'external index backend' as part of these test cases?
    # ms.build_index('name-and-age', Vertex, keys=[name, age], backing_index='search')
    # ms.commit()
    # assert tg.V.has('name', 'herc', predicate=CONTAINS).name == ['hercules']



def test_build_edge_index():
    ms = tg.management_system
    time = ms.make_property_key('time', data_type=Integer)
    rating = ms.make_property_key('rating', data_type=Decimal)
    battled = ms.make_edge_label('battled')
    ms.build_edge_index(battled, 'battles-by-time', keys=[time])
    ms.build_edge_index(battled, 'battles-by-rating-time', keys=[rating, time], direction=Direction.OUT, sort_order=Order.DESC)
    ms.commit()


def test_output_graph():
    filename = tempfile.gettempdir() + "test-graph.son"
    tg.output_graph(filename)
    assert os.path.exists(filename)


def test_input_graph():
    filename = tempfile.gettempdir() + "test-graph.son"
    temp_titan_graph = TitanFactory.build().set('storage.backend','inmemory').open()
    temp_g = Gremthon(temp_titan_graph)
    temp_g.input_graph(filename)
    assert temp_g.V.count() == 2

