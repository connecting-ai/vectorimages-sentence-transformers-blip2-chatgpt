#syntax=docker/dockerfile:1.4
FROM 484097152182.dkr.ecr.us-east-1.amazonaws.com/vectors:v8
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt
WORKDIR /src
ADD . .
EXPOSE 8080
CMD ["python", "main.py"]