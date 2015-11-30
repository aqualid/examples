#!/usr/bin/env python

import os
import sys
import argparse
import subprocess


# ==============================================================================
def _run_cmd_status(cmd, path=None):

    if path:
        env = os.environ.copy()
        env['PYTHONPATH'] = path
    else:
        env = None

    print(cmd)

    p = subprocess.Popen(cmd, env=env, shell=False)
    return p.wait()


# ==============================================================================
def _run_cmd(cmd, path=None):
    status = _run_cmd_status(cmd, path)
    if status:
        sys.exit(status)


# ==============================================================================
def _fetch_repo(cur_dir, repo_name, repo_dir=None):
    if repo_dir:
        return os.path.abspath(repo_dir)

    repo_dir = os.path.join(cur_dir, repo_name)

    default_branch = 'master'

    branch = os.environ.get('TRAVIS_BRANCH')
    if not branch:
        branch = os.environ.get('APPVEYOR_REPO_BRANCH', default_branch)

    cmd = ["git", "clone", "--depth", "1",
           "https://github.com/aqualid/%s.git" % repo_name, repo_dir]

    status = _run_cmd_status(cmd + ["-b", branch])
    if status:
        if branch == default_branch:
            sys.exit(status)

        _run_cmd(cmd + ["-b", default_branch])

    return repo_dir


# ==============================================================================
def _run_example(cmd, path, example_dir):

    cmd = cmd + ["-C", example_dir]

    _run_cmd(cmd, path)
    _run_cmd(cmd + ['-R'], path)


# ==============================================================================
def _get_examples(examples_dir):
    for item in os.listdir(examples_dir):
        example_dir = os.path.join(examples_dir, item)
        makefile = os.path.join(example_dir, 'make.aql')
        if os.path.isfile(makefile):
            yield example_dir


# ==============================================================================
def run(core_dir, tools_dir, examples_dir):

    tools_dir = os.path.join(tools_dir, 'tools')

    cmd = [sys.executable,
           "-c", "import aql;import sys;sys.exit(aql.main())",
           "-I", tools_dir]

    for example_dir in _get_examples(examples_dir):
        _run_example(cmd, core_dir, example_dir)


# ==============================================================================
def run_script(script, module_dir, examples_dir):
    cmd = [sys.executable, script]

    for example_dir in _get_examples(examples_dir):
        _run_example(cmd, module_dir, example_dir)


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
