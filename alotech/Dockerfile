FROM python:3
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
  libyaml-dev \
  vim \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY . /code/
