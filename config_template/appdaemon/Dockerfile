FROM arm32v7/python:3.6.8-alpine3.9

EXPOSE 5050

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev tzdata

RUN pip3 install appdaemon==3.0.5

CMD appdaemon -c /conf