FROM python:3.8.6-slim

# Configure for PostgreSQL
RUN apt-get update -yq && apt-get upgrade -yq
RUN apt-get install gcc python3-dev libpq-dev -yq

WORKDIR /night-owl-api
EXPOSE 5000

COPY . /night-owl-api
RUN pip install -r requirements.txt

CMD [ "sh", "start_server.sh" ]
