import json
from utils import usqs,uamzconnect
import time

# Static Locals
escalate_recipient_number = """+86low_1,+86med_2,+86high_3"""          # follow escalation path to fill in numbers
region_name = 'ap-southeast-1'
SecretName = "connectCredentials"
queue_url = "https://sqs.ap-southeast-1.amazonaws.com/997742168968/myqueue"

def lambda_handler(event, context):
    # local vars
    escalate_flag = True
    received_member = None

    if usqs.receive_queue_message(region_name = region_name,queue_url = queue_url):
        # if catches error, initiate lowest-level call
        while escalate_flag:

            for recipient in escalate_recipient_number.split(','):
                try:
                    response = uamzconnect._call_initiator(region_name,SecretName,recipient)
                    if response:    # if connected, then stop escalation
                        escalate_flag = False
                        received_member = recipient
                        break       # success contact, break loop
                except:
                    print("This call failed, continue escalate..")

            time.sleep(30)   # sleep for 30 secs before looping another round of emergency calls

    else:
        pass        # if no error to be capture, then exit program

    return {
        'statusCode': 200,
        'body': json.dumps('Call Reached Operations member number at {0}'.format(received_member))
    }



