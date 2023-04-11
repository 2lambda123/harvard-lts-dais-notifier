import logging
import os

import stomp

class ConnectionParams:
    def __init__(self, conn, queue, host, port, user, password, ack="client-individual"):
        self.conn = conn
        self.queue = queue
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ack = ack


def get_process_mq_connection(queue=None):
    logging.debug("************************ MQUTILS - GET_PROCESS_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('PROCESS_MQ_HOST')
        port = os.getenv('PROCESS_MQ_PORT')
        user = os.getenv('PROCESS_MQ_USER')
        password = os.getenv('PROCESS_MQ_PASSWORD')
        if (queue is None):
            process_queue = os.getenv('PROCESS_QUEUE_CONSUME_NAME')
        else:
            process_queue = queue
        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(host, port)])
        connection_params = ConnectionParams(conn, process_queue, host, port, user, password)
        conn.connect(user, password, wait=True)
    except Exception as e:
        logging.error(e)
        raise (e)
    return connection_params

def get_transfer_mq_connection(queue=None):
    logging.debug("************************ MQUTILS - GET_TRANSFER_MQ_CONNECTION *******************************")
    try:
        host = os.getenv('TRANSFER_MQ_HOST')
        port = os.getenv('TRANSFER_MQ_PORT')
        user = os.getenv('TRANSFER_MQ_USER')
        password = os.getenv('TRANSFER_MQ_PASSWORD')
        if (queue is None):
            process_queue = os.getenv('TRANSFER_QUEUE_CONSUME_NAME')
        else:
            process_queue = queue
        conn = stomp.Connection([(host, port)], heartbeats=(40000, 40000), keepalive=True)
        conn.set_ssl([(host, port)])
        connection_params = ConnectionParams(conn, process_queue, host, port, user, password)
        conn.connect(user, password, wait=True)
    except Exception as e:
        logging.error(e)
        raise (e)
    return connection_params

