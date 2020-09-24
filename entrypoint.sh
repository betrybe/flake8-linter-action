#!/bin/sh -l
set -x

REPOSITORY_BRANCH=$1
export GITHUB_TOKEN=$2

git clone --single-branch --branch "$REPOSITORY_BRANCH" "https://github.com/$GITHUB_REPOSITORY.git" /github/main-branch/

# Install deps and run flake8 over the student source
cd /github/workspace
python3 -m pip install -r requirements.txt
python3 -m flake8 --append-config=setup.cfg --append-config=/github/main-branch/report.cfg > /tmp/flake8.log

# Get the report and comment on PR
python3 /home/main.py /tmp/flake8.log

if [ $? != 0 ]; then
  printf "Execution error $?"
  exit 1
fi
