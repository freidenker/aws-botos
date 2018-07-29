import boto3
import os

#by env varibles get credential
ACCESS_KEY=os.environ['ACCESS_KEY']
SECRET_KEY=os.environ['SECRET_KEY']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    #aws_session_token=SESSION_TOKEN
)

client = session.client('cloudformation')
#by credential file ~/.aws/
#ec2client = boto3.client('ec2')

"""
https://boto3.readthedocs.io/en/latest/reference/services/cloudformation.html#paginators
"""

paginator = client.get_paginator('list_stacks')
response_iterator = paginator.paginate(StackStatusFilter=['DELETE_COMPLETE','CREATE_COMPLETE'])
for page in response_iterator:
    stack = page['StackSummaries']
    for output in stack:
        print (output['StackName']+" : "+output['StackStatus'])
