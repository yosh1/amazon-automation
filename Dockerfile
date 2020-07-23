FROM python:3.6-alpine

ARG project_dir=/python/app/
ADD . ${project_dir}
WORKDIR ${project_dir}

RUN set -x && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

CMD ["python3", "main.py"]