FROM python:3

WORKDIR /app
COPY app/ .

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["nameko", "run", "--config", "config.yml", "server:EventAnalyzer"]
