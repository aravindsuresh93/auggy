FROM jjanzic/docker-python3-opencv:latest

RUN pip install falcon pandas numpy gunicorn tornado

COPY . .

RUN chmod +x gateway.py file_gateway.py run.sh

CMD ./run.sh