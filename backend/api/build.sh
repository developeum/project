docker build -t itgo_api .
docker run -p 2020:8000 --detach itgo_api
