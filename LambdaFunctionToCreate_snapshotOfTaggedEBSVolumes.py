import boto3 
import collections 
import datetime 

ec = boto3.client('ec2') 
default_retaintion_days=0;


def lambda_handler(event, context): 
    
    ebs_volumes = ec.describe_volumes( Filters=[ {'Name': 'tag-key', 'Values': ['backup','Backup']}, 
                                                  {'Name': 'tag-value', 'Values': ['backup', 'Yes','yes']},                 ])   
    
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
