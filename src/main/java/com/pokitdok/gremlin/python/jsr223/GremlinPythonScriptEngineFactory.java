package com.pokitdok.gremlin.python.jsr223;

import com.tinkerpop.gremlin.Tokens;
import org.python.jsr223.PyScriptEngineFactory;

import javax.script.ScriptEngine;
import javax.script.ScriptException;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class GremlinPythonScriptEngineFactory extends PyScriptEngineFactory {

    private static final String ENGINE_NAME = "gremlin-python";
    private static final String LANGUAGE_NAME = "gremlin-python";
    private static final String VERSION_NUMBER = Tokens.VERSION;

    public String getEngineName() {
        return ENGINE_NAME;
    }

    public String getEngineVersion() {
        return VERSION_NUMBER;
    }

    public String getLanguageName() {
        return LANGUAGE_NAME;
    }

    public String getLanguageVersion() {
        return VERSION_NUMBER;
    }

    public List<String> getNames() {
        return Collections.unmodifiableList(Arrays.asList(LANGUAGE_NAME));
    }

    public String getOutputStatement(final String toDisplay) {
        return "println " + toDisplay;
    }

    public Object getParameter(final String key) {
        switch (key) {
            case ScriptEngine.ENGINE:
                return this.getEngineName();
            case ScriptEngine.ENGINE_VERSION:
                return this.getEngineVersion();
            case ScriptEngine.NAME:
                return ENGINE_NAME;
            case ScriptEngine.LANGUAGE:
                return this.getLanguageName();
            case ScriptEngine.LANGUAGE_VERSION:
                return this.getLanguageVersion();
            default:
                return null;
        }
    }

    public ScriptEngine getScriptEngine() {
        ScriptEngine engine = null;
        try {
            engine = super.getScriptEngine();
            //Load up gremthon for use within this Python script engine
            ClassLoader engineClassLoader = GremlinPythonScriptEngineFactory.class.getClassLoader();
            engine.eval(new BufferedReader(new InputStreamReader(engineClassLoader.getResourceAsStream("gremthon.py"))));
        } catch (Exception e) {
            e.printStackTrace();
        }
        return engine;
    }}