FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN rm ./*
COPY .env/ .env/
COPY model/ model/
COPY *.py ./
COPY uwsgi.ini ./
ENV LOGGER_LEVEL=INFO
ENV VERBOSE=0
# ENV UI_LOCATION=depends on deployment
# ENV LOGGER_FORMAT=see logconf.py