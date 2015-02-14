package com.pokitdok.gremlin.python.jsr223;

import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.impls.tg.TinkerGraphFactory;

import javax.script.*;
import java.io.FileNotFoundException;
import java.io.FileReader;
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

    @Test
    public void testPipeline() throws ScriptException, FileNotFoundException {
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("gremlin-python");

        engine.eval("from inspect import isfunction");
        engine.eval(new FileReader("tests/test_pipeline.py"));
        engine.eval("pipeline_tests = [v for k, v in dict(locals()).items() if isfunction(v) and k.startswith('test_')]");
        engine.eval("pipeline_tests = sorted(pipeline_tests, key=lambda f: f.func_code.co_firstlineno)");
        engine.eval("[pipeline_test() for pipeline_test in pipeline_tests]");
    }

}