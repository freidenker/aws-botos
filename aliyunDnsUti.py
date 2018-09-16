import json
import sys
import os
from datetime import datetime

#import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest, UpdateDomainRecordRequest, \
    AddDomainRecordRequest, DescribeDomainsRequest

#pip install aliyun-python-sdk-core-v3
#pip install aliyun-python-sdk-domain
#pip install aliyun-python-sdk-alidns

# create AcsClient instance
ACCESS_KEY=os.environ['ACCESS_KEY']
SECRET_KEY=os.environ['SECRET_KEY']
client = AcsClient(ACCESS_KEY,SECRET_KEY,"cn-hangzhou");


#get domamin name list
def list_domain():
    DomainList = DescribeDomainsRequest.DescribeDomainsRequest()
    DomainList.set_accept_format('json')
    DNSListJson = json.loads(client.do_action_with_exception(DomainList))
    for i in DNSListJson['Domains']['Domain']:
        print(i['DomainName'])
    #print DNSListJson



#get record name list by domain name
def list_dns_record(DomainName):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    print(DomainName+':')
#    print DomainRecordsJson
    for x in DomainRecordsJson['DomainRecords']['Record']:
         RecordId = x['RecordId']
         RR = x['RR']
         Type = x['Type']
         Line = x['Line']
         Value = x['Value']
         TTL = x['TTL']
         Status = x['Status']
         txt =  RecordId+' '+RR+' '+Type+' '+Line+' '+Value+' '+str(TTL)+' '+Status
         print(txt)
    print('\n')



#update record
def edit_dns_record(DomainName, hostname, hostname_new, Types, IP):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
            RecordId = x['RecordId']
            UpdateDomainRecord = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
            UpdateDomainRecord.set_accept_format('json')
            UpdateDomainRecord.set_RecordId(RecordId)
            UpdateDomainRecord.set_RR(hostname_new)
            UpdateDomainRecord.set_Type(Types)
            UpdateDomainRecord.set_TTL('600')
            UpdateDomainRecord.set_Value(IP)
            UpdateDomainRecordJson = json.loads(client.do_action_with_exception(UpdateDomainRecord))
            print(UpdateDomainRecordJson)


#add new record
def add_dns_record(DomainName, hostname, Types, IP):
    AddDomainRecord = AddDomainRecordRequest.AddDomainRecordRequest()
    AddDomainRecord.set_DomainName(DomainName)
    AddDomainRecord.set_RR(hostname)
    AddDomainRecord.set_Type(Types)
    AddDomainRecord.set_TTL('600')
    AddDomainRecord.set_Value(IP)
    AddDomainRecordJson = json.loads(client.do_action_with_exception(AddDomainRecord))
    print(AddDomainRecordJson)



#delete record
def delete_dns_record(DomainName, hostname):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
            RecordId = x['RecordId']
            DeleteDomainRecord = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
            DeleteDomainRecord.set_RecordId(RecordId)
            DeleteDomainRecordJson = json.loads(client.do_action_with_exception(DeleteDomainRecord))
            print(DeleteDomainRecordJson)


#set record status
def set_dns_record(DomainName, hostname, status):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
                RecordId = x['RecordId']
                SetDomainRecord = SetDomainRecordStatusRequest.SetDomainRecordStatusRequest()
                SetDomainRecord.set_accept_format('json')
                SetDomainRecord.set_RecordId(RecordId)
                SetDomainRecord.set_Status(status)
                SetDomainRecordJson = json.loads(client.do_action_with_exception(SetDomainRecord))
                print(SetDomainRecordJson)


#check record if exists
def checkRecord(recordName):
    domainNameOne=recordName.rsplit(".",2)[-1]
    domainNameTwo=recordName.rsplit(".",2)[-2]
    domainName=domainNameTwo+"."+domainNameOne
    print(domainName)
    #domainName='freidenker.tech'
    recordList=[]

    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(domainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))

    for x in DomainRecordsJson['DomainRecords']['Record']:
        #RecordId = x['RecordId']
        RR = x['RR']
        #Type = x['Type']
        #Value = x['Value']
        #Status = x['Status']
        recordItem=RR+"."+domainName
        recordList.append(recordItem)
    if(recordName in recordList):
        print(recordName + " : already existed")
        return True
    else:
        print(recordName + " : NOT exists")
        return False



list_domain()

#add_dns_record('freidenker.tech', 'test1', 'A', '10.x.1.0')
#add_dns_record('freidenker.tech', 'test2', 'A', '10.x.1.1')
#add_dns_record('freidenker.tech', 'test3', 'A', '10.x.1.2')
#add_dns_record('freidenker.tech', 'test4', 'A', '10.x.1.3')
#add_dns_record('freidenker.tech', 'test5', 'A', '10.x.1.4')
#add_dns_record('freidenker.tech', 'test6', 'A', '10.x.1.5')
#add_dns_record('freidenker.tech', 'test7', 'A', '10.x.1.6')
#add_dns_record('freidenker.tech', 'test8', 'A', '10.x.1.7')
#add_dns_record('freidenker.tech', 'test9', 'A', '10.x.1.8')
#add_dns_record('freidenker.tech', 'test10', 'A', '10.x.1.9')
#add_dns_record('freidenker.tech', 'test11', 'A', '10.x.1.10')
#add_dns_record('freidenker.tech', 'test12', 'A', '10.x.1.11')
#add_dns_record('freidenker.tech', 'test13', 'A', '10.x.1.12')
#add_dns_record('freidenker.tech', 'test14', 'A', '10.x.1.13')
#add_dns_record('freidenker.tech', 'test15', 'A', '10.x.1.14')

list_dns_record("freidenker.tech")

checkRecord("test3.freidenker.tech")
