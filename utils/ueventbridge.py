import boto3
# Event-Driven (EMR Start, EMR Close)
# on EMR start, collect alarm; config EventBridge & target SNS
# on EMR Close, delete alarm, delete EventBridge

def _get_boto_client(region_name):
    client = boto3.client('events',region_name = region_name)
    return client

def _create_emr_alarm_trigger(region_name,Name='string',
        EventPattern='string',
        State='ENABLED',
        Description='string'):
    client = _get_boto_client(region_name)
    response = client.put_rule(
        Name=Name,
        EventPattern=EventPattern,
        State=State,
        Description=Description
    )
    return response

def _delete_emr_alarm_triggers(*args,region_name):
    client = _get_boto_client(region_name)
    for arg in args:
        try:
            response = client.delete_rule(
                Name=arg
            )
        except:
            raise
    return None


def _create_emr_alarm_target(region_name,Rule='string',Id='string',Arn='string',InputPathsMap={},InputTemplate="{}",**kwargs):
    client = _get_boto_client(region_name)
    response = client.put_targets(
        Rule=Rule,
        Targets=[
            {
                'Id': Id,
                'Arn': Arn,
                'InputTransformer': {
                    'InputPathsMap': InputPathsMap,
                    'InputTemplate': InputTemplate
                },
                'RetryPolicy': {
                    'MaximumRetryAttempts': 123,
                    'MaximumEventAgeInSeconds': 123
                }
            },
        ]
    )
    return response
