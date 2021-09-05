FROM python: 3.8

RUN apt update & & apt install - y python3-opencv & & rm - rf / var/lib/apt/lists/*

RUN pip install - -upgrade pip
RUN pip install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv sync

COPY model / model/
COPY * .py ./

ENV LOGGER_LEVEL = INFO
ENV VERBOSE = 0
RUN pip freeze
# ENV UI_LOCATION=depends on deployment
# ENV LOGGER_FORMAT=see logconf.py
CMD["pipenv", "run", "start"]
