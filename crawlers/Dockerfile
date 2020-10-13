FROM ubuntu:latest

# Copy out application into container
COPY app/ /app/

# Install requirements
RUN apt-get update
RUN apt-get install -y libpq-dev python3-dev gcc python3 python3-pip cron
RUN pip3 install -r /app/requirements.txt

# Create cron task and user for that task
COPY crontab /etc/cron.d/crawler_task
RUN crontab /etc/cron.d/crawler_task

# And finally run cron
CMD ["cron", "-f"]
