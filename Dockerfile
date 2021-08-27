#c
FROM jjanzic/docker-python3-opencv:latest

RUN pip install falcon pandas numpy gunicorn

COPY . .

RUN chmod +x gateway.py

CMD gunicorn -b 0.0.0.0:8099 gateway:app --reload
