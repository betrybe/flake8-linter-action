FROM python:3.9.0-buster

RUN apt update && \
    apt -yq install apt-utils git less

COPY entrypoint.sh /home/entrypoint.sh
COPY src/ /home/
COPY requirements.txt /home/requirements.txt
COPY report.cfg /home/report.cfg

RUN python3 -m pip install -r /home/requirements.txt
RUN chmod a+x -R /home/*.py
RUN chmod a+x -R /home/entrypoint.sh

ENTRYPOINT ["/home/entrypoint.sh"]
