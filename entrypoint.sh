#!/bin/sh -l
set -x

# Run flake8 over the student source and generate a log report
cd /github/workspace
if test -f "dev-requirements.txt" ; then
  python3 -m pip install -r dev-requirements.txt
else
  python3 -m pip install -r requirements.txt
fi
python3 -m flake8 --append-config=setup.cfg --append-config=/home/report.cfg > /tmp/flake8.log

# Get the report and comment on PR
python3 /home/main.py /tmp/flake8.log

if [ $? != 0 ]; then
  printf "Execution error $?"
  exit 1
fi
