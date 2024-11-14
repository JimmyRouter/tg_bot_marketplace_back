FROM python:3.11

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

CMD ["uvicorn", "server_launcher:app","--reload", "--host", "0.0.0.0", "--port", "80"]