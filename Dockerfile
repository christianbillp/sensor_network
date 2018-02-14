#FROM python:alpine
#FROM hypriot/rpi-alpine

FROM arm32v6/alpine:3.6
ENV QEMU_EXECVE 1
COPY . /usr/bin
RUN [ "qemu-arm-static", "/bin/sh", "-c", "ln -s resin-xbuild /usr/bin/cross-build-start; ln -s resin-xbuild /usr/bin/cross-build-end; ln /bin/sh /bin/sh.real" ]

# Create folder for application
RUN mkdir /app

# Update apt sources and extra programs (python:slim)
#RUN apt update
#RUN apt install -y git python3-pip nano

# Update apt sources and extra programs (python:alpine)
RUN apk add --update git python3 nano

# Dependency for DHT22 sensor
RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git
RUN mv Adafruit_Python_DHT/Adafruit_DHT/ /app

# Dependency for MQTT communication
RUN pip3 install paho-mqtt

# Add and run application
ADD application.py /app/application.py
CMD [ "python", "/app/application.py" ]
