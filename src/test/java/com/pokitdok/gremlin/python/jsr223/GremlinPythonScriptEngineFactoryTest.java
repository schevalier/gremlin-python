package com.pokitdok.gremlin.python.jsr223;

import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.impls.tg.TinkerGraphFactory;

import javax.script.*;
import java.util.ArrayList;
import java.util.List;

import org.testng.annotations.Test;

public class GremlinPythonScriptEngineFactoryTest {

    @Test
    public void testBasicUse() throws ScriptException {
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("gremlin-python");

        Graph graph = TinkerGraphFactory.createTinkerGraph();
        List results = new ArrayList();
        ScriptContext context = engine.getContext();
        context.setAttribute("graph", graph, ScriptContext.ENGINE_SCOPE);
        context.setAttribute("results", results, ScriptContext.ENGINE_SCOPE);
        engine.eval("g = Gremthon(graph)");
        engine.eval("g.v(1).out('knows').has('name','josh').fill(results)");
        engine.eval("assert results[0].id == '4'");
    }
}