import os

from mqresources.listener.mq_connection_params import MqConnectionParams
from mqresources.listener.stomp_listener_base import StompListenerBase


class ProcessNotifyQueueListener(StompListenerBase):

    def _get_queue_name(self) -> str:
        return os.getenv('PROCESS_QUEUE_CONSUME_NAME')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('PROCESS_MQ_HOST'),
            mq_port=os.getenv('PROCESS_MQ_PORT'),
            mq_user=os.getenv('PROCESS_MQ_USER'),
            mq_password=os.getenv('PROCESS_MQ_PASSWORD')
        )

    

        
