FROM python:3.10.5

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

COPY . /app/
WORKDIR /app
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python3", "run.py"]




