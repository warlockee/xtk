# Docker Build Server

The Docker Build Server allows you to build Docker images remotely. This guide will help you set up and test the server.

## Getting Started

### Build the Docker Image

Build the Docker image using the following command:

```bash
docker build -t docker-builder:latest .
```

### Run the Docker Container

Start the Docker Build Server with:

```bash
docker run -d --name docker-builder -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /mnt/ddnfs01:/mnt/ddn \
  -v $HOME/.docker:/root/.docker \
  hub.anuttacon.com/infra/docker-builder:latest
```

**Explanation of the flags:**

- `-d`: Runs the container in detached mode.
- `--name docker-builder`: Names the container **docker-builder**.
- `-p 5000:5000`: Maps port 5000 of the host to port 5000 of the container.
- `-v /var/run/docker.sock:/var/run/docker.sock`: Allows Docker commands within the container.
- `-v /mnt/ddnfs01:/mnt/ddn`: Mounts the directory `/mnt/ddnfs01` to `/mnt/ddn` inside the container.
- `-v $HOME/.docker:/root/.docker`: Shares your Docker configurations with the container.

## Testing the Server

### Build a Docker Image

Test the build server by triggering a build:

```bash
curl -X POST http://localhost:5000/build -d '{"user": "A", "path": "/mnt/ddn/project/project-infra/infra/test", "tag": "hub.anuttacon.com/infra/helloworld:v1.0.2"}' -H "Content-Type: application/json"
```

**Parameters:**

- `"user"`: Your username or identifier.
- `"path"`: The path to the Dockerfile or project directory.
- `"tag"`: The desired tag for the built image.

### Check Build Status

Monitor the status of your build with:

```bash
curl http://localhost:5000/status/A-1731099796
```

Replace `A-1731099796` with the build ID returned from the build command.