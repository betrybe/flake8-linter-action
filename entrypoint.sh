#!/bin/sh -l
set -x

git clone --single-branch --branch "$INPUT_REPOSITORY_MAIN_BRANCH" "https://github.com/$GITHUB_REPOSITORY.git" /github/main-branch/

# Install deps
cd /github/workspace
python3 -m pip install -r requirements.txt

# Run flake8 over the student source
python3 -m flake8 --append-config=/github/main-branch/setup.cfg --append-config=/home/report.cfg > /tmp/flake8.log

# Get the report and comment on PR
cd /home
python3 main.py /tmp/flake8.log
