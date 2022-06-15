# aws-tutorials
This repo is designed for some simple helper scripts to address some issues on AWS

Tree structure of this repo:
```
|____incident_manager_lambda_function.py
|____cwlogs_driven_recaller_lambda_function.py
|____utils
| |____usnsemail.py
| |____ueventbridge.py
| |____usecrets.py
| |____usqs.py
| |____uamzconnect.py
| |____ucwlogs.py
| |____ucwalarm.py
| |______init__.py
| |______pycache__
| | |______init__.cpython-39.pyc
| | |____ucwlogs.cpython-39.pyc
| | |____ueventbridge.cpython-39.pyc
| | |____usqs.cpython-39.pyc
| | |____ucwalarm.cpython-39.pyc
| | |____uamzconnect.cpython-39.pyc
| | |____uwebhook.cpython-39.pyc
| | |____usecrets.cpython-39.pyc
| | |____usnsemail.cpython-39.pyc
| |____uwebhook.py
|____emr_manual_lambda_function.py
|____recaller_lambda_function.py
```
## How to use this repo?
In utils folder, there are some helper functions for each AWS service involved. For example, usecrets contains some functions interacting with AWS Secrets Manager.
Other functions that lie in main directory are lambda handlers. Specifically,

- incident_manager_lambda_function.py is Incident Manager lambda that handles security incidences in a centralized manner.
- cwlogs_dirven_recaller_lambda_function.py is a Recaller lambda that is based on capturing CloudWatch error logs and respond accordingly.
- emr_manual_lambda_function.py is a lambda that can automatically push and delete related alarm and event triggers based on EMR on/off states.
- recaller_lambda_function.py is a lambda that is scheduled to run, in a fixed time interval, to check if any failed notification happens, and if so, triggers re-notification and incidence escalation.




