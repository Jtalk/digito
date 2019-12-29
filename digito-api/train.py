import logconf

logconf.init_logs()

import logging

import recognition

log = logging.getLogger('train')

log.info('Training the neural network model')
recognition.prepare()
log.info('The model is successfully trained')