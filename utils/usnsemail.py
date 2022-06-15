import boto3

def _get_boto_client(region_name):
    client = boto3.client('sns',region_name = region_name)
    return client

def _send_email(region_name,message,sns_arn,Subject):
    client = _get_boto_client(region_name = region_name)
    response = client.publish(
        TargetArn=sns_arn,
        Subject=Subject,
        Message=message
    )
    return response