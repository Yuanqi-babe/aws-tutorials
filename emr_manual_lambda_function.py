from utils import ueventbridge,ucwalarm
import json
from string import Template

# Input Vars
# EMR info (from Step Fun or EventBridge，time.sleep(60*15) for 15 mins for a while if metrics is not immeidiately visible)
event = {'cluster_id':"j-3QZ49Y3KY151B"}
# Region Name
region_name = 'ap-southeast-1'


def lambda_handler(event, context):
    # ON mode
    cwalarm_name = 'sample-alarm'
    ucwalarm._create_emr_alarm(region_name=region_name,AlarmName=cwalarm_name,
                               ComparisonOperator='LessThanOrEqualToThreshold',
                               EvaluationPeriods=3,
                               MetricName='YARNMemoryAvailablePercentage',
                               Namespace='AWS/EMR',
                               Period=300,   # 5 minutes interval
                               Statistic='Maximum',
                               Threshold=20,
                               ActionsEnabled=False,
                               AlarmDescription='Yarn Memory Detector',
                               JobFlowId = event['cluster_id']
                               )
    print("create alarm success")
    cwalarm_event_pattern = json.dumps({
        "detail-type": ['CloudWatch Alarm State Change'],
        "source": ["aws.cloudwatch"],
        "detail": {
            "alarmName": [cwalarm_name]

        }
    })
    ueventbridge._create_emr_alarm_trigger(
        region_name=region_name,
        Name='sample-cwalarm-emr',
        EventPattern=cwalarm_event_pattern,
        State='ENABLED',
        Description='this is a sample EventBridge cw alarm trigger'
    )           # this is for CWAlarm, target SNS
    print("create CW rule trigger success")
    cw_input_path_map = {
            "alarmName": "$.detail.alarmName",
            "state": "$.detail.state.value",
            "previousState": "$.detail.previousState.value"
        }

    cw_input_template_map = '{"alarmName": <alarmName>,"state": <state>,"previousState": <previousState>,"Severity":"2","text-message": "Your alarm <alarmName> is changing from <previousState> to <state>"}'
    ueventbridge._create_emr_alarm_target(
        region_name=region_name, Rule='sample-cwalarm-emr', Id='sample-cwalarm-emr', Arn='arn:aws:sns:ap-southeast-1:997742168968:stepfun-failed-event-queue', InputPathsMap=cw_input_path_map, InputTemplate=cw_input_template_map
    )         # this is to associate triggers with target
    print("create CW alarm target success")

    # start EB Alarm section
    eventbrigealarm_event_pattern = json.dumps({
        "source": ["aws.emr"],
        "detail-type": ["EMR Step Status Change"],
        "detail": {
            "state": ["FAILED"]
  }
})
    ueventbridge._create_emr_alarm_trigger(
        region_name=region_name,
        Name='sample-ebalarm-emr',
        EventPattern=eventbrigealarm_event_pattern,
        State='ENABLED',
        Description='this is a sample EventBridge EventBridge alarm trigger'
    )           # this is for native EB Alarm trigger, target SNS
    print("create EB alarm rule trigger success")
    eb_input_path_map = {
            "clusterId": "$.detail.clusterId",
            "state": "$.detail.state",
            "jobName": "$.detail.name"
        }

    eb_input_template_map = '{"clusterId": <clusterId>,"jobName": <jobName>,"state": <state>,"Severity":"2","text-message": "In Cluster <clusterId> your job named <jobName> is in <state> please handle this"}'
    ueventbridge._create_emr_alarm_target(
        region_name=region_name, Rule='sample-ebalarm-emr', Id='sample-ebalarm-emr', Arn='arn:aws:sns:ap-southeast-1:997742168968:stepfun-failed-event-queue', InputPathsMap=eb_input_path_map, InputTemplate=eb_input_template_map
    )         # this is to associate triggers with target
    print("create EB alarm target success")
    #
    # # Off mode
    # ucwalarm._delete_emr_alarms('sample-alarm',region_name=region_name)         # delete CW Alarm
    # ueventbridge._delete_emr_alarm_triggers('sample-cwalarm-emr','sample-ebalarm-emr',region_name=region_name)      # dessociate triggers


if __name__ == '__main__':
    lambda_handler(event,context=None)
    # cw_input_template_map = Template('{"alarmName": <alarmName>,"state": <state>,"previousState": <previousState>,"text-message": "Your alarm <alarmName> is changing from <previousState> to <state> ${placeholder}"}').substitute(placeholder = "")
    # print(cw_input_template_map)