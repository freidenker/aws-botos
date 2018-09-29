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

ec2client = session.client('ec2')
#by credential file ~/.aws/
#ec2client = boto3.client('ec2')
response = ec2client.describe_instances()
for reservation in response["Reservations"]:
    print(str(len(reservation["Instances"])) + " is ec2 instances number")
    for instance in reservation["Instances"]:
        # This sample print will output entire Dictionary object
        #print(instance)
        # This will print will output the value of the Dictionary key 'InstanceId'
        print(instance["InstanceId"])
        print(instance['LaunchTime'])                                                                                                                                                                                                                                                                                                                                                                                                                          
