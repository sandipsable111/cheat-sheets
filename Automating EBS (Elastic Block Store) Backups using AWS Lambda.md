



Automating EBS (Elastic Block Store) Backups using AWS Lambda
















Sometimes, applications need to be backed up in order to achieve a RTO that suits customer’s business objectives.

Step1:  Setup IAM Permissions
•	Go to Services, IAM, Create a new Role
 
•	Write the name (ebs-lambda-worker)
•	Select AWS Lambda
 


•	Click Next, and Create Policy.
Use below JSON to create policy:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot",
                "ec2:CreateTags"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
 

•	Write a Policy Name, (snapshot-policy), and paste the above JSON content.
•	Refresh policies and select the above created policy.
•	Click on next and write a Role name, Role Descriptions and Create Role.
•	What we’ve just done is allowing this role to Create/Delete Snapshots, create tags and modify snapshots attributes. Also, we have allowed permissions to Describe EC2 instances and view logs in CloudWatch










Step2: Create Lambda Backup Function
1.	First script help you to create snapshot of all the volumes attached to EC2 instance:
		This first function will allow us to back up every instance in our account under the region we put the lambda function, that has a “Backup” or “backup” key tag. No need to indicate a value here.

How script works:
-	The script will search for all instances having a tag with “Backup” or “backup” on it.
-	 As soon as we have the instances list, we need to get all the EBS volumes on each instance in order to have the list of EBSs to be backed up. Also, it will look for a “Retention” tag key which will be used as a retention policy number in days. 
-	If there is no tag with that name, it will use a 7 days default value (It can be configurable in the script ) for each EBS instance.
-	After creating the snapshot, it creates a “DeleteOn” tag on the snapshot indicating when will be deleted using the Retention value and another Lambda function.







Steps to create the function:
•	Go to Services, Lambda, and click Create a Lambda Function
 

•	Just fill below required information and Skip the rest screens (like, blueprint screen, Browse serverless app repo.. )
 
•	Write a name for it (ebs-backup-worker)
•	Select Python 2.7 as a Runtime option
•	Choose or create an execution role: Select the previously created IAM role (ex. ebs-lambda-worker)
 
•	Click on Create Function
•	Paste the code below
import boto3
import collections
import datetime

ec = boto3.client('ec2')

def lambda_handler(event, context):
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['backup', 'Backup']},
        ]
    ).get(
        'Reservations', []
    )

    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    print "Found %d instances that need backing up" % len(instances)

    to_tag = collections.defaultdict(list)

    for instance in instances:
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = 7

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            print "Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId'])

            snap = ec.create_snapshot(
                VolumeId=vol_id,
            )

            to_tag[retention_days].append(snap['SnapshotId'])

            print "Retaining snapshot %s of volume %s from instance %s for %d days" % (
                snap['SnapshotId'],
                vol_id,
                instance['InstanceId'],
                retention_days,
            )


    for retention_days in to_tag.keys():
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_fmt = delete_date.strftime('%Y-%m-%d')
        print "Will delete %d snapshots on %s" % (len(to_tag[retention_days]), delete_fmt)
        ec.create_tags(
            Resources=to_tag[retention_days],
            Tags=[
                {'Key': 'DeleteOn', 'Value': delete_fmt},
            ]
        )











































2.	Second script will help you to create snapshot of particular EBS volumes:
		This function will allow us to back up particular EBS volume in our account under the region we put the lambda function, which volume has a “Backup” or “backup” key tag and value “backup”, “Yes” or “yes”.

How script works:
-	The script will search for all EBS volumes having a tag with “Backup” or “backup” with value “backup” or “Yes” or “yes” on it.
-	 As soon as we have the list of EBSs volumes to be backed up then it will look for a “Retention” tag key which will be used as a retention policy number in days. 
-	If there is no tag with that name, it will use a 7 days default value (It can be configurable in the script) for each EBS volume.
-	After creating the snapshot, it creates a “DeleteOn” tag on the snapshot indicating when will be deleted using the Retention value and another Lambda function.






Use below python script while creating lambda function:

import boto3 
import collections 
import datetime 

ec = boto3.client('ec2') #mention your region to reboot
default_retaintion_days=0;


def lambda_handler(event, context): 
    
    ebs_volumes = ec.describe_volumes( Filters=[ {'Name': 'tag-key', 'Values': 						['backup','Backup']}, 
                                                  {'Name': 'tag-value', 'Values': ['backup', 'Yes','yes']},  ])
    #print(ebs_volumes)
    
    for volume in ebs_volumes['Volumes']:
        try:
            retention_days = [
                int(tag.get('Value')) for tag in volume['Tags']
                if tag['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = default_retaintion_days
            
        print "Backing up volume- %s in AZ- %s" % (volume['VolumeId'], volume['AvailabilityZone'])
 
        # Create snapshot
        snapshot_resp = ec.create_snapshot(VolumeId= volume['VolumeId'],
                                    Description="Backup for EBS- " + volume['VolumeId']
                                )
 
        snapshot_id = snapshot_resp['SnapshotId']
        
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_on = delete_date.strftime('%Y-%m-%d')
        ec.create_tags(Resources=[snapshot_id],
                       Tags=[{'Key': 'Name', 'Value': 'snapshot' },
                             {'Key': 'DeleteOn', 'Value': delete_on},
                            ]
                    )
        print "Snapshot %s has been created and, will be deleted on %s" % (snapshot_id , delete_on)


Step3: Using CloudWatch Event - Configure Lambda to run at a defined schedule during the day
•	Open Designer and click on Add trigger
 
•	Fill below details with cron expression set time , when you want to trigger your lambda function and click on Add button. 
Step 4: Restore the created Snapshot.
•	The restoring process will remains the manual process.
•	By following below steps manually, we can restore the snapshot.
•	Select the snapshot that you want to restore.
 
•	Click on Actions, Create Volume
 

•	Fill / update the required information and click on Create Volume
•	You will see that newly created volume by selecting volume under EBS from left pane.
 
•	Then select Actions and Attach Volume
“Best practice is attach volume to the Stopped EC2 instance only”.
 


•	Select instance id to which you want to attach this volume and click on Attach.
 
•	And Restart your EC2 instance.
____________________________________________________
