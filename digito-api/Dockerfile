FROM python:3.7
RUN pip install --upgrade pip
RUN pip install 'gunicorn>=20.0.0,<21.0.0'
COPY requirements.txt ./
COPY model/ model/
COPY *.py ./
RUN pip install -r requirements.txt
ENV LOGGER_LEVEL=INFO
ENV VERBOSE=0
RUN pip freeze
# ENV UI_LOCATION=depends on deployment
# ENV LOGGER_FORMAT=see logconf.py
CMD ["gunicorn", "--workers=4", "--threads=1", "--worker-class=gthread", "--log-file=-", "--bind=0.0.0.0:80", "app:app"]