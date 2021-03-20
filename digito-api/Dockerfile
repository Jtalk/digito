FROM python:3.8

RUN pip install --upgrade pip
RUN pip install --user pipenv
COPY Pipenv ./
COPY Pipenv.lock ./
RUN pipenv sync

COPY model/ model/
COPY *.py ./

ENV LOGGER_LEVEL=INFO
ENV VERBOSE=0
RUN pip freeze
# ENV UI_LOCATION=depends on deployment
# ENV LOGGER_FORMAT=see logconf.py
CMD ["pipenv", "run", "start"]