The docker build server


docker build -t fastapi-dockerized-server:latest .


docker run -d \
  --name fastapi-dockerized-server \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /mnt/ddnfs01:/mnt/ddnfs01 \
  fastapi-dockerized-server:latest
