
FROM python:3.10

RUN apt-get update && apt-get -y install gcc git

RUN mkdir -p /usr/app/visual_novel

RUN pip install --no-cache-dir -r /usr/app/requirements.txt
WORKDIR /usr/app/visual_novel/