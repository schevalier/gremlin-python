import glob
from itertools import islice
import os
import sys

def load_gremthon_jars():
    for jar_dir in os.environ.get('GREMTHON_JAR_DIRS', '').split(':'):
        for jar in glob.glob(os.path.join(jar_dir, '*.jar')):
            if jar not in sys.path:
                sys.path.append(jar)

load_gremthon_jars()

#gremlin related imports (Java)
from com.tinkerpop.blueprints import Direction, Vertex
from com.tinkerpop.blueprints.impls.tg import TinkerGraphFactory
from com.tinkerpop.blueprints.impls.tg import TinkerEdge
from com.tinkerpop.blueprints.impls.tg import TinkerVertex
from com.tinkerpop.gremlin.java import GremlinPipeline
from com.tinkerpop.pipes.util import PipesFunction
from java.util import ArrayList, Collection, HashMap
from java.lang import Float


class GremthonEdge(object):

    def __init__(self, edge):
        self.edge = edge

    def __eq__(self, other):
        return self == other or self.edge == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_blueprints_edge(self):
        return self.edge

    @property
    def properties(self):
        return self.edge.propertyKeys

    def get_property(self, item):
        if item in self.edge.propertyKeys:
            return self.edge.getProperty(item)
        if hasattr(self.edge, item):
            return getattr(self.edge, item)
        return None

    def __getitem__(self, item):
        return self.get_property(item)

    def __getattr__(self, item):
        return self.get_property(item)

    @property
    def label(self):
        return self.edge.getLabel()

    @property
    def in_vertex(self):
        return self.edge.getVertex(Direction.IN)

    @property
    def out_vertex(self):
        return self.edge.getVertex(Direction.OUT)

    def __repr__(self):
        return '{0}'.format(self.edge)


class GremthonVertex(object):

    def __init__(self, vertex):
        self.vertex = vertex

    def __eq__(self, other):
        return self == other or self.vertex == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_blueprints_vertex(self):
        return self.vertex

    @property
    def properties(self):
        return self.vertex.propertyKeys

    def get_property(self, item):
        if item in self.vertex.propertyKeys:
            return self.vertex.getProperty(item)
        if hasattr(self.vertex, item):
            return getattr(self.vertex, item)
        return None

    def __getitem__(self, item):
        return self.get_property(item)

    def __getattr__(self, item):
        return self.get_property(item)

    def __repr__(self):
        return '{0}'.format(self.vertex)

    @property
    def edges(self):
        for edge in self.vertex.getEdges():
            yield GremthonEdge(edge)


def map_gremthon_type(obj):
    if isinstance(obj, TinkerEdge):
        return GremthonEdge(obj)
    elif isinstance(obj, TinkerVertex):
        return GremthonVertex(obj)
    elif isinstance(obj, HashMap):
        return dict(obj)
    elif isinstance(obj, ArrayList):
        return list(obj)
    else:
        return obj


class GremthonPipesFunction(PipesFunction):

    def __init__(self, function):
        self.function = function

    def compute(self, argument):
        return self.function(map_gremthon_type(argument))


class GremthonPipeline(object):

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def __iter__(self):
        for item in self.pipeline:
            yield map_gremthon_type(item)

    def __getitem__(self, item):
        if isinstance(item, int) and item >= 0:
            return islice(self, item, item + 1)
        elif isinstance(item, slice):
            return islice(self, item.start, item.stop, item.step)
        else:
            raise KeyError("Item must be non-negative number or slice (not {0})".format(item))

    def __repr__(self):
        return '\n'.join([str(item) for item in self])

    def add(self, pipe):
        self.pipeline.addPipe(pipe)
        return self

    def both(self, *args):
        if len(args) > 1 and isinstance(args[0], int):
            return self.__class__(self.pipeline.both(args[0], args[1:]))
        else:
            return self.__class__(self.pipeline.both(args))

    def both_e(self, *args):
        if len(args) > 1 and isinstance(args[0], int):
            return self.__class__(self.pipeline.bothE(args[0], args[1:]))
        else:
            return self.__class__(self.pipeline.bothE(args))

    def both_v(self):
        return self.__class__(self.pipeline.bothV())

    def E(self, key=None, value=None):
        if key and value:
            return self.__class__(self.pipeline.E(key, value))
        else:
            return self.__class__(self.pipeline.E())

    def V(self, key=None, value=None):
        if key and value:
            return self.__class__(self.pipeline.V(key, value))
        else:
            return self.__class__(self.pipeline.V())

    def has(self, key=None, value=None):
        if key is not None and value is None:
            return self.__class__(self.pipeline.has(key))
        else:
            return self.__class__(self.pipeline.has(key, value))

    def interval(self, key, start, end):
        if isinstance(start, float):
            start_value = Float(start)
        else:
            start_value = start
        if isinstance(end, float):
            end_value = Float(end)
        else:
            end_value = end
        return self.__class__(self.pipeline.interval(key, start_value, end_value))

    def id_edge(self, graph):
        return self.__class__(self.pipeline.idEdge(graph))

    def id_vertex(self, graph):
        return self.__class__(self.pipeline.idVertex(graph))

    def id(self):
        return self.__class__(self.pipeline.id())

    def in_e(self, *args):
        if len(args) > 1 and isinstance(args[0], int):
            return self.__class__(self.pipeline.inE(args[0], args[1:]))
        else:
            return self.__class__(self.pipeline.inE(args))

    def in_v(self):
        return self.__class__(self.pipeline.inV())

    def in_(self, *args):
        in_method = getattr(self.pipeline, 'in')
        if len(args) > 1 and isinstance(args[0], int):
            return self.__class__(in_method(args[0], args[1:]))
        else:
            return self.__class__(in_method(args))

    def label(self):
        return self.__class__(self.pipeline.label())

    def out_e(self, *args):
        return self.__class__(self.pipeline.outE(args))

    def out(self, *args):
        return self.__class__(self.pipeline.out(args))

    def out_v(self):
        return self.__class__(self.pipeline.outV())

    def map(self, *args):
        return self.__class__(self.pipeline.map(args))

    def property_(self, key):
        return self.__class__(self.pipeline.property(key))

    def step(self, func):
        return self.__class__(self.pipeline.step(func))

    def copy_split(self, *args):
        return self.__class__(self.pipeline.copySplit(args))

    def exhaust_merge(self):
        return self.__class__(self.pipeline.exhaustMerge())

    def fair_merge(self):
        return self.__class__(self.pipeline.fairMerge())

    def if_then_else(self, if_function, then_function, else_function):
        return self.__class__(self.pipeline.ifThenElse(if_function, then_function, else_function))

    def loop(self, step, while_function, emit_function=None):
        if emit_function:
            return self.__class__(self.pipeline.loop(step, while_function, emit_function))
        return self.__class__(self.pipeline.loop(step, while_function))

    def and_(self, *args):
        and_method = getattr(self.pipeline, 'and')
        return self.__class__(and_method(args))

    def back(self, named_step):
        return self.__class__(self.pipeline.back(named_step))

    def dedup(self, dedup_func=None):
        if dedup_func is None:
            return self.__class__(self.pipeline.dedup())
        else:
            return self.__class__(self.pipeline.dedup(dedup_func))

    def except_(self, *args):
        #TODO: debug except
        except_method = getattr(self.pipeline, 'except')
        if len(args) == 1 and isinstance(args[0], (Collection, list, tuple)):
            return self.__class__(except_method(ArrayList(args[0])))
        else:
            return self.__class__(except_method(args))

    def filter(self, filter_func):
        return self.__class__(self.pipeline.filter(GremthonPipesFunction(filter_func)))

    def or_(self, *args):
        or_method = getattr(self.pipeline, 'or')
        return self.__class__(or_method(args))

    def random(self, bias):
        return self.__class__(self.pipeline.random(bias))

    def range(self, low, high):
        return self.__class__(self.pipeline.range(low, high))

    def retain(self, *args):
        return self.__class__(self.pipeline.retain(args))

    def simple_path(self):
        return self.__class__(self.pipeline.simplePath())

    def aggregate(self):
        #TODO: handle other aggregate options
        return self.__class__(self.pipeline.aggregate())

    def optional(self, named_step):
        return self.__class__(self.pipeline.optional(named_step))

    #TODO: groupBy ?

    #TODO: groupCount ?

    def link_out(self, label, named_step_other_vertex):
        return self.__class__(self.pipeline.linkOut(label, named_step_other_vertex))

    def link_in(self, label, named_step_other_vertex):
        return self.__class__(self.pipeline.linkIn(label, named_step_other_vertex))

    def link_both(self, label, named_step_other_vertex):
        if isinstance(named_step_other_vertex, GremthonVertex):
            return self.__class__(self.pipeline.linkBoth(label, named_step_other_vertex.vertex))
        else:
            return self.__class__(self.pipeline.linkBoth(label, named_step_other_vertex))

    def side_effect(self, side_effect_func):
        return self.__class__(self.pipeline.sideEffect(side_effect_func))

    def store(self, side_effect_func):
        #TODO: handle other store variations
        return self.__class__(self.pipeline.store())

    #TODO: table ?

    #TODO: tree ?

    def gather(self, gather_function=None):
        if gather_function is None:
            return self.__class__(self.pipeline.gather())
        else:
            return self.__class__(self.pipeline.gather(GremthonPipesFunction(gather_function)))

    def memoize(self, named_step, map=None):
        if map is None:
            return self.__class__(self.pipeline.memoize(named_step))
        else:
            return self.__class__(self.pipeline.memoize(named_step, map))

    @property
    def name(self):
        return '\n'.join([item.name for item in self])

    def order(self):
        #TODO: handle other variations
        return self.__class__(self.pipeline.order())

    def path(self, *args):
        path_args = []
        for arg in args:
            if hasattr(arg, '__call__'):
                path_args.append(GremthonPipesFunction(arg))
            else:
                path_args.append(arg)
        return self.__class__(self.pipeline.path(tuple(path_args)))

    def scatter(self):
        return self.__class__(self.pipeline.scatter())

    def select(self, *args):
        select_args = []
        for arg in args:
            if hasattr(arg, '__call__'):
                select_args.append(GremthonPipesFunction(arg))
            else:
                select_args.append(arg)
        if len(select_args) >= 1 and isinstance(args[0], (Collection, list, tuple)):
            return self.__class__(self.pipeline.select(select_args[0], select_args[1:]))
        else:
            return self.__class__(self.pipeline.select(tuple(select_args)))

    def shuffle(self):
        return self.__class__(self.pipeline.shuffle())

    def cap(self):
        return self.__class__(self.pipeline.cap())

    #TODO: orderMap ?

    def transform(self, transform_func):
        return self.__class__(self.pipeline.transform(transform_func))

    def as_(self, name):
        as_method = getattr(self.pipeline, 'as')
        return self.__class__(as_method(name))

    def start(self, obj):
        return self.__class__(self.pipeline.start(obj))

    def count(self):
        return self.pipeline.count()

    def iterate(self):
        self.pipeline.iterate()

    def next(self, number):
        return self.pipeline.next(number)

    def to_list(self):
        return self.pipeline.toList()

    def fill(self, collection):
        self.pipeline.fill(collection)
        return collection

    def enable_path(self):
        self.pipeline.enablePath()
        return self

    def optimize(self, optimize):
        self.pipeline.optimize(optimize)
        return self

    def remove(self):
        self.pipeline.remove()

    def _(self):
        return self.__class__(self.pipeline._())



class Gremthon(object):

    def __init__(self, graph):
        self.graph = graph

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.graph.shutdown()

    def add_edge(self, index, out_v, in_v, label, **kwargs):
        if isinstance(out_v, GremthonVertex):
            out_v = out_v.get_blueprints_vertex()
        if isinstance(in_v, GremthonVertex):
            in_v = in_v.get_blueprints_vertex()
        e = self.graph.addEdge(index, out_v, in_v, label)
        for kw in kwargs:
            e.setProperty(kw, kwargs[kw])
        return map_gremthon_type(e)

    def add_vertex(self, index, **kwargs):
        v = self.graph.addVertex(index)
        for kw in kwargs:
            v.setProperty(kw, kwargs[kw])
        return map_gremthon_type(v)

    @property
    def E(self):
        return GremthonPipeline(GremlinPipeline(self.graph).E())

    def edges(self, key, value):
        return GremthonPipeline(GremlinPipeline(self.graph).E(key, value))

    @property
    def V(self):
        return GremthonPipeline(GremlinPipeline(self.graph).V())

    def vertices(self, key, value):
        return GremthonPipeline(GremlinPipeline(self.graph).V(key, value))

    def e(self, index):
        return GremthonPipeline(GremlinPipeline(self.graph.getEdge(index)))

    def v(self, index):
        return GremthonPipeline(GremlinPipeline(self.graph.getVertex(index)))


if __name__ == "__main__":
    graph = TinkerGraphFactory.createTinkerGraph()
    g = Gremthon(graph)
