FROM jjanzic/docker-python3-opencv:latest
RUN pip install uvicorn fastapi pyjwt passlib psycopg2 pandas python-multipart coloredlogs sqlalchemy
WORKDIR /app/auggy
