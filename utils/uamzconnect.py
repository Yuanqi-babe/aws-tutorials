# -*- coding: utf-8 -*-
import json
import boto3
from utils import usecrets

# # ENV Vars
# region_name = 'ap-southeast-1'
# SecretName = "connectCredentials"
# recipient_number = ''


def _get_boto_client(region_name):
    client = boto3.client('connect',region_name = region_name)
    return client


def _call_initiator(region_name,SecretName,recipient_number):
    try:
        client = _get_boto_client(region_name = region_name)
        info = '<speak><break time="3s"/>您好,您是猪猪吗？</speak>'
        connect_secrets_string = usecrets._get_secret(SecretName,region_name)
        response = client.start_outbound_voice_contact(
            DestinationPhoneNumber=recipient_number,
            InstanceId=  connect_secrets_string['InstanceId'],              # '3131373e-f49b-44dc-b877-6bd9f0bce65a',
            ContactFlowId= connect_secrets_string['ContactFlowId'],          # '848b1e34-0211-444a-bf51-63a92b8788c1',
            SourcePhoneNumber= connect_secrets_string['SourcePhoneNumber'],                     # '+6569942891',
            Attributes={
                'message': info
            }
        )
        return response
    except Exception:
        raise Exception("CallFailedException")


