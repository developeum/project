FROM python:3

COPY app/ /app/
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "server:app"]
