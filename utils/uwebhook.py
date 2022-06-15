import json
import logging
import os
import requests

# Read all the  variables from SNS event

# logging related code
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# invoke webhook
def _push_msg(webhook_url,**kwargs):


    # Read message posted on SNS Topic

    # Construct a new slack message
    slack_message = {
        kw:kwargs[kw] for kw, kwargs[kw] in kwargs
    }

    # Post message on SLACK_WEBHOOK_URL
    x = requests.post(webhook_url, json=slack_message)

    return {"code":"webhook post success"}