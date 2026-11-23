# Dockerized Web Application

A two-service web application built with Flask, Redis, Docker, and Docker Compose.

## What it demonstrates

- Flask serves a page-visit counter backed by Redis.
- Redis data persists in a Docker volume.
- Compose manages the app, Redis, and their health checks.
- The app runs as a non-root user and is exposed only on localhost.
- Redis has no host port exposed.

## Run

Requirements: Docker Engine and the Docker Compose plugin.

Start the app with `docker compose up --build -d`, then open
<http://localhost:5000/>. Refresh the page to increment the counter.

Check health with `curl -i http://localhost:5000/health`.
View logs with `docker compose logs --tail=50`.

Stop the containers and keep Redis data with `docker compose down`.
To also delete Redis data, run `docker compose down --volumes`.

## Verification performed

- The health endpoint returned `{"redis":"connected","status":"healthy"}`.
- Compose reported both services healthy.
- The counter increased from 16 to 18 after container recreation, confirming
  data persisted in the Redis volume. The volume was later removed with
  `docker compose down --volumes`.
