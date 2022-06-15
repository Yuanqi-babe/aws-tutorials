import boto3


def _get_boto_client(region_name):
    client = boto3.client('cloudwatch',region_name = region_name)
    return client

def _create_emr_alarm(region_name,AlarmName='Web_Server_CPU_Utilization',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=60,
        Statistic='Average',
        Threshold=70.0,
        ActionsEnabled=False,
        AlarmDescription='Default Alarm Description',**kwargs):
    # Create CloudWatch client, kwargs contains a series of dimension required name and value.
    client = _get_boto_client(region_name)

    # parse kw args
    dim_args_dict = {}
    for kw in kwargs:
        dim_args_dict[kw] = kwargs[kw]

    # Create alarm
    client.put_metric_alarm(
        AlarmName=AlarmName,
        ComparisonOperator=ComparisonOperator,
        EvaluationPeriods=EvaluationPeriods,
        MetricName=MetricName,
        Namespace=Namespace,
        Period=Period,
        Statistic=Statistic,
        Threshold=Threshold,
        ActionsEnabled=ActionsEnabled,
        AlarmDescription=AlarmDescription,
        Dimensions=[
            {'Name':kw,'Value':args} for kw,args in dim_args_dict.items()
        ]
    )

def _delete_emr_alarms(*args,region_name):
    # Delete alarm
    arg_list = []
    for arg in args:
        arg_list.append(arg)
    client = _get_boto_client(region_name)
    response = client.delete_alarms(
        AlarmNames=arg_list,
    )
    return response