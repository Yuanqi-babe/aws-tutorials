from utils import uamzconnect

# -*- coding: utf-8 -*-
import json
import boto3
from utils import uamzconnect,uwebhook,usnsemail
from string import Template

# ENV Vars
region_name = 'ap-southeast-1'
SecretName = "connectCredentials"
recipient_number = """+86low_1"""          # follow escalation path to fill in numbers
webhook_url = "http://samplehook.com"
email_sns_arn = "arn:aws:sns:ap-southeast-1:997742168968:stepfun-failed-event-queue"

# Events are from SNS Events
# TODO: add sample

def lambda_handler(event, context):

    # get required input from EventBridge incidence JSON, then map action
    severity_level = event['Records'][0]['Sns']['Message']['Severity']
    message = event['Records'][0]['Sns']['Message']['text-message']
    aws_sns_event_type = event['Records'][0]['Sns']['event_type']
    subject = Template("[Severity ${severity_level}] ${aws_sns_event_type}").substitute(severity_level = severity_level,aws_sns_event_type = aws_sns_event_type)


    if int(severity_level) == 1:
        # trigger Amazon Connect Lambda, trigger webhook Lambda, trigger Email Lambda
        uamzconnect._call_initiator(region_name=region_name,SecretName=SecretName,recipient_number=recipient_number)
        # TODO: webhook keyword arguments
        uwebhook._push_msg(webhook_url=webhook_url)
        # TODO: email
        usnsemail._send_email(region_name = region_name,message=message,sns_arn=email_sns_arn,Subject=subject)
    elif int(severity_level) == 2:
        # trigger webhook Lambda, trigger Email Lambda
        # TODO: webhook keyword arguments
        uwebhook._push_msg(webhook_url=webhook_url)
        # TODO: email
        usnsemail._send_email(region_name = region_name,message=message,sns_arn=email_sns_arn,Subject=subject)
    elif int(severity_level) == 3:
        # TODO: email
        usnsemail._send_email(region_name = region_name,message=message,sns_arn=email_sns_arn,Subject=subject)
    else:
        pass
        print("Severity not valid")

    return {
        'statusCode': 200,
        'body': json.dumps("Incidence Handled")

    }
