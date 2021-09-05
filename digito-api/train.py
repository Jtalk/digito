import logconf
import recognition
import logging


log = logging.getLogger('train')

log.info('Training the neural network model')
recognition.train()
log.info('The model is successfully trained')
