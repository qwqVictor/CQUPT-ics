FROM python:3.10.6-slim

EXPOSE 80
WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements_server.txt /tmp/requirements_server.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt -r /tmp/requirements_server.txt

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]