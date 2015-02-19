package com.pokitdok.gremlin.python.jsr223;

import com.tinkerpop.blueprints.Edge;
import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.Vertex;
import org.python.jsr223.PyScriptEngine;

import javax.script.*;
import java.io.Reader;

public class GremlinPythonScriptEngine implements ScriptEngine, Compilable, Invocable, AutoCloseable {
    private final ScriptEngine python;

    public GremlinPythonScriptEngine(ScriptEngine scriptEngine) {
        this.python = scriptEngine;
    }

    @Override
    public Object eval(String script, ScriptContext context) throws ScriptException {
        return this.python.eval(script, context);
    }

    @Override
    public Object eval(Reader reader, ScriptContext context) throws ScriptException {
        return this.python.eval(reader, context);
    }

    @Override
    public Object eval(String script) throws ScriptException {
        return this.python.eval(script);
    }

    @Override
    public Object eval(Reader reader) throws ScriptException {
        return this.python.eval(reader);
    }

    @Override
    public Object eval(String script, Bindings n) throws ScriptException {
        inject_gremthon(n);
        return this.python.eval(script, n);
    }

    @Override
    public Object eval(Reader reader, Bindings n) throws ScriptException {
        inject_gremthon(n);
        return this.python.eval(reader, n);
    }

    @Override
    public void put(String key, Object value) {
        this.python.put(key, value);
    }

    @Override
    public Object get(String key) {
        return this.python.get(key);
    }

    @Override
    public Bindings getBindings(int scope) {
        return this.python.getBindings(scope);
    }

    @Override
    public void setBindings(Bindings bindings, int scope) {
        inject_gremthon(bindings);
        this.python.setBindings(bindings, scope);
    }

    @Override
    public Bindings createBindings() {
        Bindings bindings = this.python.createBindings();
        inject_gremthon(bindings);
        return bindings;
    }

    private void inject_gremthon(Bindings bindings) {
        if (!bindings.containsKey("Gremthon")) {
            try {
                //Load up Gremthon into these Bindings
                this.python.eval("from gremthon import Gremthon, GremthonVertex, GremthonEdge", bindings);
            } catch (ScriptException e) {
                e.printStackTrace();
            }
        }

        if (bindings.containsKey("g") && bindings.get("g") instanceof Graph) {
            try {
                //wrap `g` with Gremthon to pick up nice python language support
                this.python.eval("g = Gremthon(g)", bindings);
            } catch (ScriptException e) {
                e.printStackTrace();
            }
        }

        if (bindings.containsKey("v") && bindings.get("v") instanceof Vertex) {
            try {
                //wrap `v` with GremthonVertex to pick up nice python language support
                this.python.eval("v = GremthonVertex(v)", bindings);
            } catch (ScriptException e) {
                e.printStackTrace();
            }
        }

        if (bindings.containsKey("e") && bindings.get("e") instanceof Edge) {
            try {
                //wrap `e` with GremthonEdge to pick up nice python language support
                this.python.eval("e = GremthonEdge(e)", bindings);
            } catch (ScriptException e) {
                e.printStackTrace();
            }
        }

    }

    @Override
    public ScriptContext getContext() {
        return this.python.getContext();
    }

    @Override
    public void setContext(ScriptContext context) {
        this.python.setContext(context);
    }

    @Override
    public ScriptEngineFactory getFactory() {
        return this.python.getFactory();
    }

    @Override
    public void close() throws Exception {
        ((PyScriptEngine)this.python).close();
    }

    @Override
    public CompiledScript compile(String script) throws ScriptException {
        return ((PyScriptEngine)this.python).compile(script);
    }

    @Override
    public CompiledScript compile(Reader script) throws ScriptException {
        return ((PyScriptEngine)this.python).compile(script);
    }

    @Override
    public Object invokeMethod(Object thiz, String name, Object... args) throws ScriptException, NoSuchMethodException {
        return ((PyScriptEngine)this.python).invokeMethod(thiz, name, args);
    }

    @Override
    public Object invokeFunction(String name, Object... args) throws ScriptException, NoSuchMethodException {
        return ((PyScriptEngine)this.python).invokeFunction(name, args);
    }

    @Override
    public <T> T getInterface(Class<T> clasz) {
        return ((PyScriptEngine)this.python).getInterface(clasz);
    }

    @Override
    public <T> T getInterface(Object thiz, Class<T> clasz) {
        return ((PyScriptEngine)this.python).getInterface(thiz, clasz);
    }
}
