import os

from mqresources.listener.mq_connection_params import MqConnectionParams
from mqresources.listener.stomp_listener_base import StompListenerBase


class TransferNotifyQueueListener(StompListenerBase):

    def _get_queue_name(self) -> str:
        return os.getenv('TRANSFER_QUEUE_CONSUME_NAME')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('TRANSFER_MQ_HOST'),
            mq_port=os.getenv('TRANSFER_MQ_PORT'),
            mq_user=os.getenv('TRANSFER_MQ_USER'),
            mq_password=os.getenv('TRANSFER_MQ_PASSWORD')
        )


        
