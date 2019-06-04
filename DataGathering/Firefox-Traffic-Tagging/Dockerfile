FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y \
 vnc4server \
 jwm \
 firefox \
 tcpdump \
 nano \
 python

ADD startup_script.sh /startup_script.sh
RUN chmod +x /startup_script.sh

ADD mypass /mypass
ADD FirefoxAddon/webudptagger.py /
RUN chmod u+x /webudptagger.py
RUN mkdir /Addon
ADD FirefoxAddon/label_traffic.js /Addon
ADD FirefoxAddon/manifest.json /Addon
RUN mkdir -p /root/.mozilla/native-messaging-hosts/
ADD FirefoxAddon/webudptagger.json /root/.mozilla/native-messaging-hosts/

#Set environment variables
ENV DISPLAY :0

CMD ./startup_script.sh
