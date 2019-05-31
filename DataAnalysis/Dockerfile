FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y install python \
	python-numpy \
	python-matplotlib \
	python-scapy \
	python-sklearn

RUN mkdir /sidechannel_health
WORKDIR /sidechannel_health
ADD Makefile /sidechannel_health
ADD DataGatheringLayer.py /sidechannel_health
ADD FeatureExtractionLayer.py /sidechannel_health
ADD MachineLearningLayer.py /sidechannel_health
ADD ThreatModellingLayer.py /sidechannel_health
ADD ReactiveLayer.py /sidechannel_health
ADD ProtocolVulnerabilities /sidechannel_health/ProtocolVulnerabilities
ADD PlaintextProtocolAnalyzers /sidechannel_health/PlaintextProtocolAnalyzers
ADD examples /sidechannel_health/examples
ADD Visualizations /sidechannel_health/Visualizations

RUN mkdir /www
RUN mkdir /www/img
ADD BootstrapCSS/css /www/css
ADD BootstrapCSS/js /www/js

WORKDIR /sidechannel_health
CMD bash
