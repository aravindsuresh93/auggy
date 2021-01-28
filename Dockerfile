FROM jjanzic/docker-python3-opencv:latest

RUN pip install falcon pandas numpy gunicorn tornado

RUN apt-get update && apt-get install -y vim

COPY . .

RUN chmod +x gateway.py file_gateway.py run.sh

CMD ./run.sh