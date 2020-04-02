FROM arm32v7/python:3.8.2-buster

EXPOSE 5050

# RUN pip3 install appdaemon==4.0.2 # Last published version doesn't work
RUN pip3 install git+git://github.com/home-assistant/appdaemon.git@e82bd7cd63e8f972315b4606f63d8e91227f4da5

CMD appdaemon -c /conf