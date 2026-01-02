# Adapted from: https://fastapi.tiangolo.com/deployment/docker/#create-the-fastapi-code
FROM python:3.13
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./main.py /code/main.py
COPY ./agents /code/agents
SHELL ["/bin/bash", "-c"]
CMD python -m uvicorn main:app --port $PORT