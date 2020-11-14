FROM ubuntu:latest

# Copy our application into container
WORKDIR /app
COPY app/ .

# Install requirements
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-dev gcc cron
RUN apt-get clean
RUN pip3 install --no-cache-dir -r requirements.txt

# Create cron task
COPY crontab /etc/cron.d/crawler_task
RUN crontab /etc/cron.d/crawler_task

# And finally run cron
ENTRYPOINT ["cron", "-f"]
