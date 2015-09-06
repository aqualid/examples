#!/usr/bin/env python

import os
import sys
import subprocess


# ==============================================================================
def _run_cmd(cmd, path=None):

    if path:
        env = os.environ.copy()
        env['PYTHONPATH'] = path
    else:
        env = None

    print(cmd)

    p = subprocess.Popen(cmd, env=env, shell=False)
    result = p.wait()

    if result:
        sys.exit(result)


# ==============================================================================

def _run_example(core_dir, tools_dir, example_dir):
    tools_dir = os.path.join(tools_dir, 'tools')

    cmd = [sys.executable, "-c", "import aql;import sys;sys.exit(aql.main())", "-C", example_dir, "-I", tools_dir]
    _run_cmd(cmd, core_dir)
    _run_cmd(cmd + ['-R'], core_dir)


# ==============================================================================

def _get_examples(examples_dir):
    for item in os.listdir(examples_dir):
        example_dir = os.path.join(examples_dir, item)
        makefile = os.path.join(example_dir, 'make.aql')
        if os.path.isfile(makefile):
            yield example_dir


# ==============================================================================

def run(core_dir, tools_dir, examples_dir):
    for example_dir in _get_examples(examples_dir):
        _run_example(core_dir, tools_dir, example_dir)


# ==============================================================================

def main():
    examples_dir = os.path.abspath(os.path.dirname(__file__))

    tools_dir = os.path.join(examples_dir, 'tools')
    core_dir = os.path.join(examples_dir, 'aqualid')

    _run_cmd(["git", "clone", "-b", "master", "--depth", "1", "https://github.com/aqualid/aqualid.git"])
    _run_cmd(["git", "clone", "-b", "master", "--depth", "1", "https://github.com/aqualid/tools.git"])

    run(core_dir, tools_dir, examples_dir)


# ==============================================================================
if __name__ == '__main__':
    main()
