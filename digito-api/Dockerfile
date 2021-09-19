FROM python:3.8

RUN apt update && apt install -y python3-opencv && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv sync

COPY *.py ./

ENV LOGGER_LEVEL=INFO
ENV VERBOSE=0
RUN pip freeze

# from deployment
ENV UI_LOCATION=
ENV TF_SERVING_LOCATION=

# see logconf.py
ENV LOGGER_FORMAT= 
CMD ["pipenv", "run", "start"]
