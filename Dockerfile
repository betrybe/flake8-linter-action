FROM alpine:3.12.0

RUN apk --update add python3 && \
    apk add py3-pip && \
    apk add coreutils && \
    apk add git less openssh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/*

COPY entrypoint.sh /home/entrypoint.sh
COPY src/ /home/
COPY requirements.txt /home/requirements.txt
COPY report.cfg /home/report.cfg

RUN python3 -m pip install -r /home/requirements.txt
RUN chmod a+x -R /home/*.py
RUN chmod a+x -R /home/entrypoint.sh

ENTRYPOINT ["/home/entrypoint.sh"]
