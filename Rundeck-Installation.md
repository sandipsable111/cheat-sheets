3.	Rundeck
3.1.	Rundeck Installation
	Update OS
		$ sudo yum update
	Rundeck requires java, install open JDK use the following command:
		$ sudo yum install java-1.8.0-openjdk java-1.8.0-openjdk-devel -y
	 Execute the following command to install the Rundeck rpm package
             $ sudo rpm -Uvh http://repo.rundeck.org/latest.rpm
	 Finally, run the below command to install Rundeck
$ sudo yum install rundeck
	Installed Rundeck version is ‘Rundeck 3.3.5’ 
		
3.2.	Customize Rundeck Setup Configuration    
	Open the framework.properties file and modify it as below
$ sudo vi /etc/rundeck/framework.properties
Change below 


	Now open rundeck-config.properties file and replace the value of the grails.serverURL by the IP Address of your Rundeck server
			$ sudo vi /etc/rundeck/rundeck-config.properties
	Now restart the Rundeck Service
$  sudo service rundeckd restart
	 If you are using Firewall, make sure to open the port 4440
			 $ sudo firewall-cmd --zone=public --add-port=4440/tcp –permanent
			 $ sudo firewall-cmd –reload

3.3.	Logging Into Rundeck
	 Navigate to http://Your_Server_IP_Address:4440/ in your favorite browser. the Default username is admin and the password is admin
3.4.	Run Ansible Playbook From Rundeck
1.	Once you logged in into Rundeck create new project
2.	Setup Project
-	Create a new project, and give it a name, label and description
 


3.	Once project is created, the project view in the WebGUI provides a more functional interface.
 
4.	Now setup remote node (Ansible controller node)
•	We are doing Password less SSH setup to connect to Ansible controller node.
First, we need to convert your private key from OpenSSH to RSA. Your private key will probably be in the format of OPENSSH, but Rundeck needs this to be converted to the RSA format to establish connection with the particular node/remote machine.
You can see the contents of your private key using 
       $ cat path/to/.ssh/id_rsa
And if you see the start and end of the key have the following, then your private key is in the wrong format for Rundeck and you need to change the format.
 
You need to run below command, it will update the format of your private key.
  	$ ssh-keygen -p -m PEM -f  /path/to/.ssh /id_rsa
This will rewrite the existing OPENSSH private key to the RSA format and you can see the start and end of the key similar like below.
 
5.	Add this generated SSH key to the ssh-agent
•	With the help of following command start the ssh-agent in the background 
$ eval $(ssh-agent -s)
•	Add your SSH private key to the ssh-agent
$ ssh-add path/to/.ssh/id_rsa
•	Reload/restart the SSHD service
	$ sudo service sshd reload
6.	Add this newly created RSA SSH private key into the Rundeck’s Key Storage.
•	Copy and paste the new RSA Private key into the 
Key Storage -> Add or Upload a Key Window
 
 
•	Click on save to add this key into key storage.
7.	 Add/Configure ansible controller node into your project.
•	Select your project from the left pane.
•	Select ‘PROJECT SETTINGS -> Edit Nodes…’
 
•	Select       -> File
•	Fill the required details 
File path: /var/lib/rundeck/resources/ {Your_project_name} /etc/resourse.xml

 
Tick the check boxes:
	 Generate : it will create resourse.xml file
	 Writable : It will allow you to edit the created file , so 		that latter on we can add more nodes into it as an 		when required.
•	Click on save to save this file configuration
•	Click on save to save the sources configurations
•	Select Edit tab to edit this above created file then select modify 

 
           
•	Add/configure your Ansible controller node into this file 
 
•	Save the modified resourse.xml file.
•	You can see that newly added node in the list of all nodes under ‘NODES’ option
 
 Make sure all nodes is displayed as a search term and you should see the nodes you entered.
•	Update the default node executor settings for the project
		Open Project Settings -> Edit Configuration	
		Select Default Node Executor at the top
		In the SSH Key Storage Path Select the storage location of your 		credentials here in this case it is: keys/ansible. And SSH 				Authentication type must be “privateKey”	 
•	Save the configuration
8.	Create a job to run ansible playbook 
•	Select JOBS option under selected project 
•	Then select create a new job 
 




•	Add job details
 
•	Then switch to workflow tab 
 
•	Under Add a step section select Command step type 
 


•	Add the same command which you have used to run Valhalla-micro-api-.yml playbook locally on that ansible node (refer point 2.3.6).
ansible-playbook -i path/to/inventory_file/hosts.py path/to/playbook/ valhalla-micro-api.yml  -e  target = valhalla-micro-api
 
•	Save the step
•	Then Switch to the node tab
 
	Select radio ‘Dispatch to Nodes’
	Select node Filter criteria to All Nodes
	Select Ansible Controller node from the list of Matched Nodes.
			 
	Click on Ansible controllers host name / IP address.
•	Finally, click on create button it will create a job 
 
•	You can run the job by clicking on   button.
•	Once you clicked on Run Job Now button Rundeck will connect using SSH to that configured Ansible controller node and, it will execute the command which we have configured as a part of this job’s steps. 
•	And deploy Valhalla-micro API on targeted remote machines as per Ansible steps/tasks has been written.
