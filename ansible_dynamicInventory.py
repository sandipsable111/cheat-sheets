#!/usr/bin/python2.7
import json
from json import JSONEncoder
import sys

#Class variables
tagKey='Env'
instanceState='running'
ansibleUser='ansible'

try:
   import boto3
except Exception as e:
    print(e)
    print(" Please rectify above exception and then try again")
    sys.exit(1)

#Class created to hold all groups and its host details
class AllGroups():
    #This smethod is used to add attributes to this class at runtime
    def addAttr(self,newAttr,attrValue):
        setattr(self, newAttr, attrValue)


# This is required to Serialize AllGroups class into JSON
class AllGroupsEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


#Get All the distinct tag values present for perticular Key
def get_tag_values(ec2_ob,tagName,state):
    stateFilter={'Name': 'instance-state-name','Values': [state]}

    tags=[]
#    for i in ec2_ob.instances.all():
    for i in ec2_ob.instances.filter(Filters=[stateFilter]):
#        print("\tTags:")
        for idx, tag in enumerate(i.tags, start=1):
            if(tag['Value'] not in tags and tag['Key']== tagName):
               # print("\t- [{0}] Key: {1}\tValue: {2}".format(idx,tag['Key'],tag['Value'] ))
                tags.append(tag['Value'])
    return tags


#Get all list of hosts tagged under same tag value
def get_hosts(ec2_ob,tagName,tagValue,state):
    f ={"Name": "tag:"+tagName, "Values": [tagValue]}
    f1={'Name': 'instance-state-name','Values': [state]}

    hosts=[]
    for each_in in ec2_ob.instances.filter(Filters=[f,f1]):
       # print(each_in.private_ip_address)
         hosts.append(each_in.private_ip_address)

    return hosts

#This is the main method from here actual execution starts
def main():

        ec2_ob=boto3.resource("ec2","ap-south-1")
        ec2_tags=get_tag_values(ec2_ob,tagKey,instanceState)
       # print(json.dumps(ec2_tags))
        all_hosts=AllGroups()

        #Grouping hosts by their tag value
        for tagValue in ec2_tags:
           # print("Getting host for tagValue : "+tagValue)
            db_group=get_hosts(ec2_ob,tagKey,tagValue,instanceState)
            host={
                    'hosts': db_group,
                    'vars':  {
                        'group_name': tagValue+' seerver group',
                        'ansible_user': ansibleUser
                        }
                    }
            all_hosts.addAttr(tagValue,host)
            #For loop ends here

        print (json.dumps(all_hosts,indent=3, cls=AllGroupsEncoder))

        return None

if __name__=="__main__":
    main()
