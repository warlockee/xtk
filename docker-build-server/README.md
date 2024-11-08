The docker build server

To start:

docker build -t docker-builder:latest .


docker run -d --name docker-builder -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock -v /mnt/ddnfs01:/mnt/ddn -v $HOME/.docker:/root/.docker hub.anuttacon.com/infra/docker-builder:latest

To test:
curl -X POST http://localhost:5000/build -d '{"user": "A", "path": "/mnt/ddn/project/project-infra/infra/test", "tag": "hub.anuttacon.com/infra/helloworld:v1.0.2"}' -H "Content-Type: application/json"


curl http://localhost:5000/status/A-1731099796