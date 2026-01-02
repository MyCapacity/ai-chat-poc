# Introduction
The Advanced Analytics agent can be tested locally via the ADK web UI or deployed as a web service.

## ADK agent development kit
To test agents using the ADK web UI, run `adk web backend\agents --port 8080`.

## Web service development 
The Advanced Analytics web service is broken up into two servers, a FastAPI backend that connects to Vertex AI and a Next.js frontend that talks to the backend. Both need to be running for the production server to work. Run these commands to start the servers:
* backend: `python main.py`
* frontend: `npx next dev -p 8080`

The backend requires Python 3.13 and the packages in requirements.txt to be installed.
The frontend requires `npx` but can install dependencies automatically.

# Deploying to GCP
Docker Compose handles deployment through the services defined in `compose.yaml`. There is also a `compose-dev.yaml` configuration which sets things up on your local machine. Each yaml file has a command at the top of it that tells you how to run it.

Requirements:
* Docker Engine (via Docker for WIndows)
* Up-to-date gcloud (`gcloud components update`)

Docker Compose automatically makes services available to each other via DNS. This lets the frontend query the backend as `http://advanced-analytics-backend` and not worry about its real IP.

testing a change 2