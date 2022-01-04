#!/bin/sh -l

# Run flake8 over the student source and generate a log report
if test -f "dev-requirements.txt" ; then
  python3 -m pip install -r dev-requirements.txt
else
  python3 -m pip install -r requirements.txt
fi
python3 -m flake8 --append-config=setup.cfg --append-config=/home/report.cfg > /tmp/flake8.log
