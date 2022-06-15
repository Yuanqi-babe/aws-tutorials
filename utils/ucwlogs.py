import boto3
from datetime import datetime, timedelta
import time

# # ENV Vars
# region_name = 'ap-southeast-1'
# exception_list = "[ERROR] DestinationNotAllowedException,[ERROR] CallFailedException"       # use comma as separator
# logGroupName = "/aws/lambda/connect-test"

def _get_boto_client(region_name):
    client = boto3.client('logs',region_name = region_name)
    return client

# For more than one Streams, e.g. latest 1
def _error_catcher(region_name,logGroupName,exception_list):
    client = _get_boto_client(region_name = region_name)
    stream_response = client.describe_log_streams(
            logGroupName=logGroupName, # Can be dynamic
            orderBy='LastEventTime',                 # For the latest events
            limit=1                                 # only get last invoke
            )


    for log_stream in stream_response["logStreams"]:
        print(log_stream["logStreamName"])
        latestlogStreamName = log_stream["logStreamName"]

        response = client.get_log_events(
                 logGroupName=logGroupName,
                 logStreamName=latestlogStreamName,
                startTime=int((datetime.today() - timedelta(hours=24)).timestamp())*1000,
                endTime=int((datetime.today() + timedelta(hours=24)).timestamp())*1000,
            )

        for event in response['events']:
            for exception in exception_list.split(','):
                if exception in event['message']:
                    # if exception matches capture criteria, then return true;
                    return True
                else:
                    pass

        return False                # else, if no error matches, return false






# query = "fields @timestamp, @message | parse @message \"username: * ClinicID: * nodename: *\" as username, ClinicID, nodename | filter ClinicID = 7667 and username='simran+test@abc.com'"
# query = """fields @message
#     | parse @message "[*] *" as loggingType, loggingMessage
#     | filter loggingType = "Container"
#     | display loggingMessage"""
# log_group = '/aws/codebuild/cicd-test'
#
# start_query_response = client.start_query(
#     logGroupName=log_group,
#                 startTime=int((datetime.today() - timedelta(hours=10000)).timestamp())*1000,
#                 endTime=int((datetime.today() + timedelta(hours=1000)).timestamp())*1000,
#     queryString=query,
# )
#
# query_id = start_query_response['queryId']
#
# response = None
#
# while response == None or response['status'] == 'Running':
#     print('Waiting for query to complete ...')
#     time.sleep(1)
#     response = client.get_query_results(
#         queryId=query_id
#     )
#     print(response)