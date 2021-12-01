Rundeck Installation:
https://docs.rundeck.com/downloads.html

https://www.decodingdevops.com/install-rundeck-on-centos-7/

#Debian/Ubuntu Install
https://computingforgeeks.com/install-and-configure-rundeck-on-ubuntu-18-04-lts/
https://gaurav.koley.in/2018/install-and-setup-rundeck-on-ubuntu

$ sudo apt update
$ sudo apt upgrade -y
#sudo apt-get install openjdk-8-jdk-headless
$ sudo apt install openjdk-8-jdk-headless
#Fix broken installation
$ java -version

wget https://dl.bintray.com/rundeck/rundeck-deb/rundeck_3.3.4.20201007-1_all.deb
$ sudo dpkg -i rundeck_3.3.4.20201007-1_all.deb
			OR
$ sudo dpkg -i rundeck*.deb

#  Configure Rundeck 
$ sudo vi /etc/rundeck/framework.properties
      Replace localhost with your server IP address 

$ sudo vi /etc/rundeck/rundeck-config.properties

$ sudo sudo systemctl start rundeckd
$ sudo sudo systemctl enable rundeckd
$ sudo systemctl status rundeckd

$ netstat -nlp   # Rundeck started on default port 4440

Use "admin" as a default username and password to login.

____________________________________________________________________________________________________

# RedHat8 / Centos - Yum RPM Install
sudo rpm -Uvh http://repo.rundeck.org/latest.rpm
sudo yum install libselinux-python
sudo yum install rundeck java

###RedHat7.7   ########################################################

sudo yum install java-1.8.0-openjdk java-1.8.0-openjdk-devel -y
sudo rpm -Uvh http://repo.rundeck.org/latest.rpm
sudo yum install rundeck



Below Steps are commomn for all :
# IMP: Do all the required configurations first and then start Rundeck service.
# Configure Rundeck 
# Note: Below Configuration and restart of service is required every time if your puplic IP of VM/Instance is not fixed.

$ sudo vi /etc/rundeck/framework.properties
      Replace localhost with your server IP address 

$ sudo vi /etc/rundeck/rundeck-config.properties

$ sudo service rundeckd start 
$  sudo service rundeckd restart 
$ service --status-all
$ netstat -nlp | grep 4440

		OR
sudo yum install java-1.8.0
sudo rpm -Uvh https://repo.rundeck.org/latest.rpm
sudo yum install rundeck
sudo service rundeckd start
sudo service rundeckd restart 
netstat -nlp | grep 4440

## Configuration

#See Logs
tail -f /var/log/rundeck/service.log
    
#Replace localhost to server IP	
sudo vi /etc/rundeck/framework.properties
sudo vi /etc/rundeck/rundeck-config.properties

– # RHEL7.7 - If you are using Firewall, make sure to open the port 4440
sudo firewall-cmd --zone=public --add-port=4440/tcp --permanent
sudo firewall-cmd --reload

#################################################################################

#Refer below blog for further steps to start with Rundeck, really it is very nicely written , Thanks to David

https://tech.davidfield.co.uk/rundeck-3-install-setup-and-an-example-project/

#Generate RSA private key it is required if you want to connect to ansible controller node using rundeck:
	#Run below command on Ansible controller and generated private key (id_rsa) in rundeck key storage
	ssh-keygen -p -m PEM -f /path/to/openssh/key
    eval $(ssh-agent -s)		
	ssh-add ~/.ssh/id_rsa
    sudo service sshd reload

	
#### If you are installing Rundeck and Ansible on same machine then follow below mandatory steps:

### Creating groups and adding users 
	sudo groupadd testuser
	sudo usermod -a -G testuser ssabale
	sudo usermod -a -G testuser rundeck
	
	#How do you know which users are already a member of a group? You can do this the old-fashioned way like so:

		grep editorial /etc/group


## Uninstall Rundeck ###
 sudo systemctl stop rundeckd
 sudo systemctl status rundeckd
 sudo yum remove rundeck 
 sudo rm -rf /etc/rundeck  /var/log/rundeck /var/lib/rundeck

#Uninstall Java 
rpm -qa | grep java

rpm -qa | grep jdk

sudo yum remove jdk1.7.0  # use this 
or  
rpm -e jdk1.7.0 

