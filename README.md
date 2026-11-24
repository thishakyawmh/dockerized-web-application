# Dockerized Web Application

A small two-service application built with Flask, Redis, Docker, and Docker Compose. It demonstrates containerized application delivery, health checks, persistent data, and a basic CI/CD pipeline.

## Architecture

- **Flask + Gunicorn** serves the web page and health endpoint.
- **Redis** stores the page-visit counter in a persistent named volume.
- **Docker Compose** manages service startup, health checks, restart policies, and the internal network.
- The web container runs as a non-root user, binds to localhost on the host, has a read-only root filesystem, drops Linux capabilities, and uses a restricted temporary filesystem.
- Redis is not published to the host network and stores data in the named volume.

## Requirements

- Docker Engine
- Docker Compose plugin
- Python 3.12+ (only needed to run the unit tests outside Docker)

## Run

Start the stack:

```bash
docker compose up --build -d
```

Open <http://localhost:5000/> and refresh to increment the Redis-backed visit counter.

Check health:

```bash
curl -i http://localhost:5000/health
docker compose ps
docker compose logs --tail=50
```

Stop containers while preserving Redis data:

```bash
docker compose down
```

Delete the Redis volume as well:

```bash
docker compose down --volumes
```

## Run unit tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

The test suite covers page-visit increments and healthy/unhealthy Redis responses without requiring a running Redis service.

## CI/CD

GitHub Actions runs the Python unit tests, builds the Docker Compose stack, checks the application health endpoint, and verifies that the Redis counter increments. A successful push to `main` also builds and publishes an image to GitHub Container Registry using a commit-SHA tag and the `latest` tag.

Dependabot checks Python, Docker image, and GitHub Actions dependencies weekly.

## Configuration and security

The sample application requires no application secrets. Keep Redis internal to the Compose network. The web service is bound to `127.0.0.1` by default; change that deliberately if you need external access, and place a reverse proxy with TLS and appropriate access controls in front of it.
