FROM tensorflow/serving:2.6.0

COPY model /models/model/1

EXPOSE 80

CMD ["--model_name=model", "--rest_api_port=80"]