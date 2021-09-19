import logging
import requests

log = logging.getLogger('net')


class TensorflowClient:

    def __init__(self, url: str):
        self.url = url

    def recognise(self, image):
        body = {'instances': image.tolist()}
        response = requests.post(self.url + '/models/model:predict',
                                 json=body)
        json_response = response.json()
        if 'error' in json_response:
            message = json_response['error'][:200] + "..." + json_response['error'][-200:] if len(
                json_response['error']) > 400 else json_response['error']
            log.error('Error querying Tensorflow Serve: ' + message)
            raise Exception('Error querying Tensorflow Serve')
        return json_response['predictions']

    def status(self):
        response = requests.get(self.url + '/models/model')
        json_response = response.json()
        status = json_response["model_version_status"][0]
        value = status["status"]
        if status.get("state", "") != "AVAILABLE" or value.get("error_code", "") != "OK":
            raise Exception(
                "Error in downstream service (Tensorflow Serving): " + value["error_message"])
