#!/usr/bin/env python

import os
import sys

def _run_cmd(cmd):
    print(cmd)
    result = os.system(cmd)
    if result:
      sys.exit(result)

def _run_example(core_dir, tools_dir, example_dir):
    cmd = "PYTHONPATH='%s' python -c 'import aql;import sys;sys.exit(aql.main())' -C '%s' -I '%s'" % (core_dir, example_dir, tools_dir)
    _run_cmd(cmd)
    _run_cmd(cmd + ' -R')

def _get_examples(examples_dir):
    for item in os.listdir(examples_dir):
        example_dir = os.path.join(examples_dir, item)
        makefile = os.path.join(example_dir, 'make.aql')
        if os.path.isfile(makefile):
            yield example_dir

def run(core_dir, tools_dir, examples_dir):
    for example_dir in _get_examples(examples_dir):
        _run_example(core_dir, tools_dir, example_dir)

if __name__ == '__main__':

    examples_dir = os.path.abspath(os.path.dirname(__file__))
    tools_dir = os.path.join(examples_dir, 'tools', 'tools')
    core_dir = os.path.join(examples_dir, 'aqualid')

    _run_cmd("git clone -b pytest --depth 1 https://github.com/aqualid/aqualid.git")
    _run_cmd("git clone -b pytest --depth 1 https://github.com/aqualid/tools.git")

    run(core_dir, tools_dir, examples_dir)
