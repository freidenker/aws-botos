import os
import boto3
from datetime import datetime

ACCESS_KEY=os.environ['ACCESS_KEY']
SECRET_KEY=os.environ['SECRET_KEY']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    #aws_session_token=SESSION_TOKEN
)

ec2client = session.client('ec2')
#ec2client = boto3.client('ec2')
response = ec2client.describe_instances()
instanceId=''
for reservation in response["Reservations"]:
    print(str(len(reservation["Instances"])) + " is ec2 instances number")
    for instance in reservation["Instances"]:
        # This sample print will output entire Dictionary object
        #print(instance)
        # This will print will output the value of the Dictionary key 'InstanceId'
        instanceId=instance["InstanceId"]
        print("get instance id: " + instance["InstanceId"])
        #print(instance['LaunchTime'])


cwclient = session.client('cloudwatch')
monitorResponse = cwclient.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instanceId
        },
    ],
    StartTime=datetime(2018, 1, 6),
    EndTime=datetime(2018, 1, 7),
    Period=360,
    Statistics=[
        'Average',
    ],
    Unit='Percent')


print(len(monitorResponse['Datapoints']))
print(monitorResponse['Datapoints'][0])