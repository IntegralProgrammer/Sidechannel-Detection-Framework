FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y install openssh-server tcpdump python

RUN useradd -ms /bin/bash ubuntu
RUN bash -c 'echo -e "ubuntu\nubuntu" | passwd ubuntu'

ADD logging_shell.py /logging_shell.py

CMD bash -c 'service ssh start; /bin/bash'
