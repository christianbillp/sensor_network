FROM python:slim

# Update apt sources and extra programs
RUN apt update
RUN apt install -y git python3-pip nano

# Dependency for DHT22 sensor
RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git
RUN mv Adafruit_Python_DHT/Adafruit_DHT/ /app

# Dependency for MQTT communication
RUN pip3 install paho-mqtt

# Add and run application
RUN mkdir /app 
ADD application.py /app/application.py
CMD [ "python", "/app/application.py" ]
