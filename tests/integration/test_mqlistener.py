import json
import logging
import os
import sys
import time
from collections import OrderedDict
from unittest.mock import patch
import mqutils

sys.path.append('app')

from mqresources.listener.process_notify_queue_listener import ProcessNotifyQueueListener
from mqresources.listener.transfer_notify_queue_listener import TransferNotifyQueueListener

queue_name = "/queue/test-dais-notify"


@patch("mqresources.listener.process_notify_queue_listener.ProcessNotifyQueueListener._handle_received_message")
@patch("mqresources.listener.process_notify_queue_listener.ProcessNotifyQueueListener._get_queue_name")
def test_process_listener(get_queue_name_mock, handle_received_message_mock):
    '''Tests to see if the listener picks up a message from the process queue'''
    get_queue_name_mock.return_value = queue_name
    mq_listener_object = ProcessNotifyQueueListener()

    message_json = notify_email_process_message()

    counter = 0
    # Try for 30 seconds then fail
    while not handle_received_message_mock.call_count:
        time.sleep(2)
        counter = counter + 2
        if counter >= 10:
            assert False, "test_listener: could not find anything on the {} after 30 seconds".format(queue_name)

    args, kwargs = handle_received_message_mock.call_args
    assert type(args[0]) is dict
    assert OrderedDict(args[0]) == OrderedDict(message_json)

    # cleanup the queue and disconnect the listener
    mq_listener_object._acknowledge_message(args[1], args[2])
    mq_listener_object.disconnect()

@patch("mqresources.listener.transfer_notify_queue_listener.TransferNotifyQueueListener._handle_received_message")
@patch("mqresources.listener.transfer_notify_queue_listener.TransferNotifyQueueListener._get_queue_name")
def test_transfer_listener(get_queue_name_mock, handle_received_message_mock):
    '''Tests to see if the listener picks up a message from the process queue'''
    get_queue_name_mock.return_value = queue_name
    mq_listener_object = TransferNotifyQueueListener()

    message_json = notify_email_transfer_message()

    counter = 0
    # Try for 30 seconds then fail
    while not handle_received_message_mock.call_count:
        time.sleep(2)
        counter = counter + 2
        if counter >= 10:
            assert False, "test_listener: could not find anything on the {} after 30 seconds".format(queue_name)

    args, kwargs = handle_received_message_mock.call_args
    assert type(args[0]) is dict
    assert OrderedDict(args[0]) == OrderedDict(message_json)

    # cleanup the queue and disconnect the listener
    mq_listener_object._acknowledge_message(args[1], args[2])
    mq_listener_object.disconnect()

def notify_email_process_message():
    '''Creates a dummy queue json message to notify the queue that an email needs to be sent'''
    try:
        # Details needed to send the message.
        message_json = {
            "subject": "Process Queue Test Email",
            "body": "Process Queue Test Email Body"
        }

        # Default to one hour from now
        now_in_ms = int(time.time()) * 1000
        expiration = 36000000 + now_in_ms

        print("msg json:")
        print(message_json)
        message = json.dumps(message_json)
        connection_params = mqutils.get_process_mq_connection(queue_name)
        connection_params.conn.send(queue_name, message, headers={"persistent": "true", "expires": expiration})
        print("MESSAGE TO QUEUE notify_email_process_message")
        print(message)
    except Exception as e:
        print(e)
        raise e
    return message_json

def notify_email_transfer_message():
    '''Creates a dummy queue json message to notify the queue that an email needs to be sent'''
    try:
        # Details needed to send the message.
        message_json = {
            "subject": "Transfer Queue Test Email",
            "body": "Transfer Queue Test Email Body"
        }

        # Default to one hour from now
        now_in_ms = int(time.time()) * 1000
        expiration = 36000000 + now_in_ms

        print("msg json:")
        print(message_json)
        message = json.dumps(message_json)
        connection_params = mqutils.get_transfer_mq_connection(queue_name)
        connection_params.conn.send(queue_name, message, headers={"persistent": "true", "expires": expiration})
        print("MESSAGE TO QUEUE notify_email_process_message")
        print(message)
    except Exception as e:
        print(e)
        raise e
    return message_json
