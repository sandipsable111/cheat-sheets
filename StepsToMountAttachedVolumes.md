##Commands to run Cloud formation templates: ##

   Postgres EC2 Instance Creation:
	#Mster:
	aws cloudformation create-stack --stack-name postgresdbec2stack --template-body file://postgres-db-ec2-template.yml --parameters file://postgres-db-ec2-parameters.json

	#Slaves in AZ2a
	aws cloudformation create-stack --stack-name postgresdbslaveAz2a --template-body file://postgres-db-slave-az2a-ec2-template.yml --parameters file://postgres-db-slave-az2a-ec2-parameters.json

	#Slaves in AZ2b
	aws cloudformation create-stack --stack-name postgresdbslaveAz2b --template-body file://postgres-db-slave-az2b-ec2-template.yml --parameters file://postgres-db-slave-az2b-ec2-parameters.json

## Host file Special char issue resolution ##
	https://www.programmersought.com/article/8935375251/

##Commands to generate self signed certs and NGINX SSL cert configuration :## 
 
	-> $ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/key.key -out /etc/ssl/cert.crt
	
	-> And update cert and file mode to chmod 644 ../key  ../cert.crt

##Command / Steps to mount Attached volumes: ##

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html#ebs-mount-after-reboot

	STEP1:  The following is example output for a T2 instance. The root device is /dev/xvda. The attached volume is /dev/xvdb, which is not yet mounted.

		->$ lsblk
		NAME                     MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
		xvda                     202:0    0   15G  0 disk
		├─xvda1                  202:1    0    1M  0 part
		└─xvda2                  202:2    0   15G  0 part /
		xvdb                     202:16   0  3.9T  0 disk
		xvdf                     202:80   0  200G  0 disk
		└─xvdf1                  202:81   0   20G  0 part
		  ├─appvg-nessuslv       253:0    0    2G  0 lvm  /opt/nessus_agent
		  ├─appvg-varsaltcachelv 253:1    0    2G  0 lvm  /var/cache/salt
		  ├─appvg-Taniumlv       253:2    0    7G  0 lvm  /opt/Tanium
		  └─appvg-crowdstrikelv  253:3    0  200M  0 lvm  /opt/CrowdStrike

	#Step2:  Use the file -s command to get information about a specific device, such as its file system type. If the output shows simply data, as in the following example output, there is no file system on the device

		->$ sudo file -s /dev/xvdb
		/dev/xvdb: data

	#STEP3: Use the lsblk -f command to get information about all of the devices attached to the instance.

		->$ sudo lsblk -f
		NAME               FSTYPE   LABEL UUID                                   MOUNTPOINT
		xvda
		├─xvda1
		└─xvda2            xfs            5a000634-a1fc-****   /
		xvdb
		xvdf
		└─xvdf1            LVM2_mem       6Cx4gh-Aw2y-****
		  ├─appvg-nessuslv xfs            31903df9-8d69-****   /opt/nessu
		  ├─appvg-varsaltcachelv
						   xfs            9155faee-d916-****   /var/cache
		  ├─appvg-Taniumlv xfs            78ff350a-29e6-****   /opt/Taniu
		  └─appvg-crowdstrikelv
						   xfs            12c555c4-d9e0-****   /opt/Crowd
						   
	#STEP4:  If you have an empty volume, use the mkfs -t command to create a file system on the volume.
		->$ sudo mkfs -t xfs /dev/xvdb
		If you get an error that mkfs.xfs is not found, use the following command to install the XFS tools and then repeat the previous command:
		-> $ sudo yum install xfsprogs
		
	#STEP5: Use the mkdir command to create a mount point directory for the volume. or you can mount the volume to an
			existing directory.
			-> $ sudo mkdir /data

	#STEP6: Use the following command to mount the volume at the directory you created in the previous step.
		-> $ sudo mount /dev/xvdb /data
		
	#STEP7: sudo cp /etc/fstab /etc/fstab.orig
	#STEP8: ls -la /etc | grep fstab
	#STEP8: sudo blkid
	#STEP9: sudo vi /etc/fstab
		Add the following entry by updating UUID value and mount point directory path:
			UUID=a65c153d-a736-****  /data  xfs  defaults,nofail  0  2
			
	#STEP10: sudo umount /data
	#STEP11: sudo lsblk -f    # Test /data unmounted successfully
	#STEP12: sudo mount -a    # Test /data mounted back successfully this time it is mounted by refering the entry that 
							   # we had added into the /etc/fstab file.
	#STEP13:  sudo lsblk -f    # Test /data mounted successfully.
