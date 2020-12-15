FROM python:3

WORKDIR /app
COPY app/ .

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "server:app"]
