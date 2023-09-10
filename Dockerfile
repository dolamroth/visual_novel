
FROM python:3.10

RUN apt-get update && apt-get -y install gcc git

RUN mkdir -p /usr/app/visual_novel

COPY ./requirements.txt /usr/app/visual_novel/requirements.txt
RUN pip install --no-cache-dir -r /usr/app/visual_novel/requirements.txt
RUN pip install gunicorn
WORKDIR /usr/app/visual_novel/
