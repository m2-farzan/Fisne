FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install iproute2 iputils-ping python3 python3-flask iptables -y
# RUN sysctl -w net.ipv4.ip_forward=1  --> Sometimes needed

RUN mkdir /ui
COPY . /ui
WORKDIR /ui
ENTRYPOINT ["python3", "ui.py"]