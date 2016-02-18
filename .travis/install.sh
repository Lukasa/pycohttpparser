#!/bin/bash

set -e
set -x

# temporary pyenv installation to get latest pypy before container infra upgrade
# now using the -latest because of a segfault bug we're encountering in 2.6.1
if [[ "${TOXENV}" = pypy* ]]; then
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    PYENV_ROOT="$HOME/.pyenv"
    PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    pyenv install pypy-4.0.1
    pyenv global pypy-4.0.1
fi

python -m pip install .
python -m pip install -r test_requirements.txt
python -m pip install flake8
