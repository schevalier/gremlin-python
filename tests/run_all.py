#utility script to run all tests within a `mvn test` run
import glob
import imp
from inspect import isfunction
import os

for module_file_path in glob.glob('tests/*.py'):
    module_path, module_filename = os.path.split(module_file_path)
    if module_filename.startswith('test_'):
        module_name, file_ext = os.path.splitext(module_filename)
        module = imp.load_source(module_name, module_file_path)
        test_functions = [getattr(module, attr) for attr in dir(module) if isfunction(getattr(module, attr)) and attr.startswith('test_')]
        test_functions = sorted(test_functions, key=lambda f: f.func_code.co_firstlineno)
        for test_function in test_functions:
            test_function()
