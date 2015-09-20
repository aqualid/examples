#!/usr/bin/env python

import os
import sys
import argparse
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
def _fetch_repo(cur_dir, repo_name, repo_dir=None):
    if repo_dir:
        return os.path.abspath(repo_dir)

    repo_dir = os.path.join(cur_dir, repo_name)

    _run_cmd(["git", "clone", "-b", "master", "--depth", "1",
              "https://github.com/aqualid/%s.git" % repo_name, repo_dir])

    return repo_dir


# ==============================================================================

def _run_example(core_dir, tools_dir, example_dir):
    tools_dir = os.path.join(tools_dir, 'tools')

    cmd = [sys.executable, "-c", "import aql;import sys;sys.exit(aql.main())",
           "-C", example_dir, "-I", tools_dir]
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
def _parse_args():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('--core-dir', action='store',
                             dest='core_dir', metavar='PATH',
                             help="Aqualid core directory. "
                                  "By default it will be fetched from GitHub.")

    args_parser.add_argument('--tools-dir', action='store',
                             dest='tools_dir', metavar='PATH',
                             help="Aqualid tools directory. "
                                  "By default it will be fetched from GitHub.")

    return args_parser.parse_args()


# ==============================================================================

def main():
    args = _parse_args()

    examples_dir = os.path.abspath(os.path.dirname(__file__))

    core_dir = _fetch_repo(examples_dir, 'aqualid', args.core_dir)
    tools_dir = _fetch_repo(examples_dir, 'tools', args.tools_dir)

    run(core_dir, tools_dir, examples_dir)


# ==============================================================================
if __name__ == '__main__':
    main()
