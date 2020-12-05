FROM python:3.7-slim

RUN apt-get update -yq && apt-get upgrade -yq

WORKDIR /night-owl-api
EXPOSE 5000

COPY . /night-owl-api
RUN pip install -r requirements.txt

CMD [ "sh", "start_server.sh" ]
