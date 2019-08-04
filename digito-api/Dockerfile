FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN rm /app/*
COPY ./ /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nose2
RUN rm -r tests
ENV LOGGER_LEVEL=INFO
ENV VERBOSE=0
# ENV UI_LOCATION=depends on deployment
# ENV LOGGER_FORMAT=see logconf.py