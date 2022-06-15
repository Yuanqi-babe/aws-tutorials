import logging
import boto3
from botocore.exceptions import ClientError
import json


# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

def _get_boto_client(region_name):
    client = boto3.client('sqs',region_name = region_name)
    return client


def send_queue_message(region_name, queue_url, msg_attributes, msg_body):
    """
    Sends a message to the specified queue.
    """
    try:
        sqs_client = _get_boto_client(region_name)
        response = sqs_client.send_message(QueueUrl=queue_url,
                                           MessageAttributes=msg_attributes,
                                           MessageBody=msg_body)
    except ClientError:
        logger.exception(f'Could not send meessage to the - {queue_url}.')
        raise
    else:
        return response

def receive_queue_message(region_name,queue_url):
    """
    Retrieves one or more messages (up to 10), from the specified queue.
    """
    try:
        sqs_client = _get_boto_client(region_name)
        response = sqs_client.receive_message(QueueUrl=queue_url,
                                              AttributeNames=[
                                                  'SentTimestamp'
                                              ],
                                              MaxNumberOfMessages=1,
                                              MessageAttributeNames=[
                                                  'All'
                                              ],
                                              VisibilityTimeout=0,
                                              WaitTimeSeconds=0
                                              )
    except ClientError:
        logger.exception(
            f'Could not receive the message from the - {queue_url}.')
        raise
    else:
        return response

def delete_queue_message(region_name, queue_url, receipt_handle):
    """
    Deletes the specified message from the specified queue.
    """
    try:
        sqs_client = _get_boto_client(region_name)
        response = sqs_client.delete_message(QueueUrl=queue_url,
                                             ReceiptHandle=receipt_handle)
    except ClientError:
        logger.exception(
            f'Could not delete the meessage from the - {queue_url}.')
        raise
    else:
        return response