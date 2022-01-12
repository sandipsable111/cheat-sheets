# RED-HAT CheatSheet
# Sudo user creation 
https://linuxconfig.org/redhat-8-add-user-to-sudoers

In this section we will be creating a new sudo user account.
#Gain root command line access:
$ sudo su

#Use the useradd command to create a new user eg. ansible and add user to the wheel group.
$ useradd -G wheel ansible

#Set password to new ansible:
$ passwd ansible

#Re-login we the new sudo user to apply the new settings:
$ su ansible

#Test sudo permissions:
$ sudo whoami
root

# add user as sudo user without password
sudo echo "rundeck ALL=(ALL) NOPASSWD:ALL">> /etc/sudoers

### Creating groups and adding users 
	sudo groupadd testuser
	sudo usermod -aG testuser ssabale
	sudo usermod -aG testuser rundeck
	sudo usermod -aG wheel rundeck
	#How do you know which users are already a member of a group? 
		$ groups ssabale  # Will print all the group names
		
		
#Description	Abreviation	Octal code
	Read access							r	4
	Write (change) permission			w	2
	Execute script of binary executable	x	1
	Read and Execute					rx	5
	Read and Write						rw	6
	Read, Write and Execute				rwx	7

	Ex. chmod 640 filename
	          (rw-r-----) 
	
## chmod  file permissions explained: 
	
-rw-rw-r--
	First  rw-  Owner or craetor permissions can read write
	Second rw-  Group permissions can read write
	Third  r--  All other users and group permissions can read only


#List running services
https://www.cyberciti.biz/faq/check-running-services-in-rhel-redhat-fedora-centoslinux/
service --status-all
service --status-all | more
service --status-all | grep ntpd
service --status-all | less

# Check the running process ID
ps -ef | grep -v grep | grep -w spring-boot-rest-example | awk '{print $2}'


cat /etc/passwd | cut -d: -f1

 
#####How to create tar.gz file in Linux using command line

	$ tar -czvf file.tar.gz directory
#Verify tar.gz file using the ls command and tar command

	$ ls -l projects.tar.gz
	$ tar -ztvf projects.tar.gz
	
##Untar tar file by skipping mentioned number of parent direrctory levels "--strip-components 3"
	$ tar -xf vertica-client-9.3.1-x86_64.tar.gz -C Destination_dir_path  --strip-components 3


#Iptables Essentials: Common Firewall Rules and Commands:
https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands
$ sudo iptables -S
$ sudo iptables -A INPUT -p tcp -m  --dport 4440 -m conntrack --ctstate NEW,UNTRACKED,ESTABLISHED -j ACCEPT
