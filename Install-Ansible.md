#Install Ansible 
Note: 
Since Ansible 2.10 for RHEL is not available at this time, continue to use Ansible 2.9.


	#On RHEL 7.7
		sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
		            OR
		sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
		
		#Execute below command if required #For RHEL-7 only
		subscription-manager repos --enable "rhel-*-optional-rpms" --enable "rhel-*-extras-rpms"  --enable "rhel-ha-for-rhel-*-server-rpms" 
		
		sudo yum install ansible
		ansible --version

		To enable the Ansible Engine repository for RHEL 7, run the following command:
             #Can skip below step.		
			sudo subscription-manager repos --enable rhel-7-server-ansible-2.9-rpms
			
	#On RHEL/CentOS8
		sudo yum update --nobest
		sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm 
		              OR 
		yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
		
		#Execute below command if required #For RHEL-8 only
		subscription-manager repos --enable "codeready-builder-for-rhel-8-$(arch)-rpms" 
		
		sudo yum install ansible
		ansible --version
	
        #Python3 and Install Pywinrm if you have windows OS target host machines.
		sudo pip install pywinrm
		OR
		sudo pip install "pywinrm>=0.3.0"  / sudo pip3 install "pywinrm>=0.3.0"
		


#USed below command to see your inventory is able to read all vault encrypted variables of not: 

Below is used for default inventory file :
sudo ansible -m debug -a 'var=hostvars[inventory_hostname]' all

If you want to call it for your inventory file then use below 
sudo ansible -i your/inventory/filepath/ownInventory  -m debug -a 'var=hostvars[inventory_hostname]' all

 
export ANSIBLE_VAULT_PASSWORD_FILE=/etc/ansible/jenkins_coe/.vault_pass.txt

sudo ansible-playbook temp_deploy_service.yml -i temp_hosts.yml


drwx------ 4 root    root     4096 Sep 16 15:27 .ansible


FinkitResourcesVM- 10.1.0.22
TechCOEDevOPsJenkins- 10.1.0.4



/etc/ansible/ansibleVault/vault_secrete.txt


#Installing ansible 

$ sudo apt update
$ sudo apt install software-properties-common
$ sudo apt-add-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible

ansible --version

############ Dynamic Inventory ###########################################
Python

Step 1
sudo apt-get update -y
Step 2
sudo apt-get install -y python-boto3
sudo apt-get install -y python-boto

sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install python3-pip
pip3 install boto3

pip install --upgrade requests==2.20.1

Add new IMA role with EC2ReadOnlyAccess/Ec2FullAccess policy

Must add your Python installation path on top of the py inventory file 
  ## Install latesr python versiion minimum 
			python3.6
  ## Upgrade your PIP installer first if it is not updated 
		$ sudo pip install --upgrade pip
  ## Install boto3 using 
		$ sudo pip install boto3
  ## TO read variables from yaml file we need to install PyYAML
		pip install -U PyYAML


Ping hosts using dynamic inventory :

$ ansible -i aws_dyn_inv_copy.py proxy -m ping

To run playbook using dynamic inventory with dynamic host / host group name use below command:

 $ ansible-playbook -i aws_dyn_inv.py      playbook.yml -e target=db
 $ ansible-playbook -i aws_dyn_inv_copy.py playbook.yml -e target='db'
 
 $ ansible-playbook -i aws_dyn_inv_new.py site.yml -e target=redhat
 
#List out all the tasks
 $ ansible-playbook site.yml --list-tasks -e target=redhat 
 
 #Run Playbook from perticular tasks 

 $ ansible-playbook  -i aws_dyn_inv_new.py site.yml -e target=redhat --start-at-task="Read-write git checkout from github"

 
 #Your playbook should have below declaration for hosts :
 - name: update web servers
  hosts:  "{{ target }}"
  remote_user: ssabale
  
  
##### Ansible Vault Config #############################################
Step1: Follow the standard folder structure 
	Ex. you should have 
						your_playbook.yml	
						group_vars
						-> all
							-> vars.yml
							-> vault.yml      #You can encrypt this file using $ansible-vault encrypt 
											 This file holds all the secrets.
						-> [your_group_name]
							-> vars.yml
							-> vault.yml

Step2: Create one txt file which holds your ansible-vault password and keep it at users home directory.
		ex. create .vault_pass.txt 
		
Step3: Edit ansible.cf file and point vault_password_file path to the path of your .vault_pass.txt file.

Step4: All set start using ansible-vault without entering password. 

  
################ Ansible Folder Structure Creation :
 
#sudo mkdir -p inventories/{production,staging,partner}/{group_vars,host_vars}
sudo touch inventories/{production,staging,partner}/hosts.py
sudo mkdir -p group_vars host_vars library module_utils filter_plugins
sudo mkdir -p roles/common/{tasks,handlers,templates,files,vars,defaults,meta,library,module_utils,lookup_plugins}
sudo touch site.yml roles/common/{tasks,handlers,templates,files,vars,defaults,meta}/main.yml
sudo touch  webserver-ui.yml webserver-api.yml webserver-lb.yml

sudo mkdir -p ./{group_vars,host_vars}
sudo touch  ./{group_vars,host_vars}/vars.yml vault.yml


###################### Run Playbook with dynamic inventory ####################################

https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Github SSH connection:

Step1: Generate SSH key if you don't have it. ssh-keygen -t rsa
Step2: Copy generated ssh public key into your github account
       Settings -> SSH and GPG keys -> New SSH key and paste your copied public key there.
	   
Step3: Start ssh agent and your newly generated/ existing private ssh key into their list
	   eval `ssh-agent -s`
	   ssh-add .ssh/id_rsa.github
	   
	   
	   
########################### Shell Script to run Ansible playbook from remote location ##################

#!/bin/bash

echo "connecting to Ansible Controller"

ssh -t ansible@10.0.0.237 'ansible-playbook -i /etc/ansible/migration/puppet_migration/aws_dyn_inv_new.py /etc/ansible/migration/puppet_migration/site.yml -e target=redhat; exit;  bash -l '

echo "Playbook Execution completed..."
	   
###########################################################################################

ansible-playbook -i /opt/sandip/ansible/puppet_migration/aws_dyn_inv_new.py /opt/sandip/ansible/puppet_migration/sitebkp1.yml -e target=localhost -vv

################### Set Python default version for all users ##########################################################
alternatives --list | grep -i python
alternatives --install /usr/bin/python python /usr/bin/python2.7 1
alternatives --install /usr/bin/python python /usr/bin/python3.6 2
alternatives --install /usr/bin/python python /usr/local/bin/python3.7 3
alternatives --config python

###Install Ansible for python3  ###

python3 -m pip install ansible  OR
pip3 install ansible







