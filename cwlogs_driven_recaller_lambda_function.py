import json
from utils import ucwlogs,uamzconnect
import time

# ENV Vars
escalate_recipient_number = """+86low_1,+86med_2,+86high_3"""          # follow escalation path to fill in numbers
time_out_for_emergency_loops =  10            # units: number of loops

def lambda_handler(event, context):
    # local vars
    escalate_flag = True
    received_member = None

    if ucwlogs._error_catcher():
        # if catches error, initiate lowest-level call
        while escalate_flag:

            loop_count = 1
            if loop_count == time_out_for_emergency_loops:
                break       # enforced break loop when time out reaches

            for recipient in escalate_recipient_number.split(','):
                try:
                    response = uamzconnect._call_initiator(recipient)
                    if response:    # if connected, then stop escalation
                        escalate_flag = False
                        received_member = recipient
                        break       # success contact, break loop
                except:
                    print("This call failed, continue escalate..")

            time.sleep(30*60)   # sleep for 30 mins before looping another round of emergency calls
            loop_count += 1     # record num of loops

    else:
        pass        # if no error to be capture, then exit program

    return {
        'statusCode': 200,
        'body': json.dumps('Call Reached Operations member number at {0}'.format(received_member))
    }



