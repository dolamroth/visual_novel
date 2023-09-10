
FROM python:3.10

RUN apt-get update && apt-get -y install gcc git
RUN git config --global --add safe.directory /usr/app

RUN mkdir -p /usr/app/visual_novel
COPY ./requirements.txt /usr/app/visual_novel/requirements.txt

RUN pip install --no-cache-dir -r /usr/app/visual_novel/requirements.txt
RUN pip install --no-cache-dir gunicorn

WORKDIR /usr/app/visual_novel/

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

