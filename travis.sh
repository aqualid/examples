set -ex

git clone --depth 1 https://github.com/aqualid/aqualid.git

PYTHONPATH=$PWD/aqualid coverage run --source=tools tests/run.py

flake8 --max-complexity=9 `find tools -name "[a-zA-Z]*.py"`
flake8 `find tests -name "[a-zA-Z]*.py"`


git clone --depth 1 https://github.com/aqualid/examples.git

PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_hello -I $PWD/tools
PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_hello -I $PWD/tools -R
PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_generator -I $PWD/tools
PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_generator -I $PWD/tools -R
PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_libs -I $PWD/tools
PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_libs_1 -I $PWD/tools
PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_libs_2 -I $PWD/tools
PYTHONPATH=$PWD/aqualid python -c "import aql;import sys;sys.exit(aql.main())" -C examples/cpp_libs_2 -I $PWD/tools -R

