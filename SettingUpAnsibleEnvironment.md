## Install Ansible Steps on RHEL 

sudo yum -y install @development   # Step-1

#sudo yum install python36  - Can be Skip
#sudo yum install python-pip  - Can be Skip
python3 -m ensurepip --upgrade - - Can be Skip
sudo yum install python-pip python-wheel - Can be Skip
sudo yum upgrade python-setuptools     - Can be Skip
pip3 install --user -U setuptools - Can be Skip

pip3 install --user --upgrade setuptools  - Step-2

pip3 install --user ez_setup  - Can be Skip
python3 -m pip install --user --upgrade pip  - Can be Skip

pip3 install --user ansible  -  Step-3 

ansible --version

	  ansible [core 2.11.4]
	  config file = None
	  configured module search path = ['/home/ec2-user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
	  ansible python module location = /home/ec2-user/.local/lib/python3.6/site-packages/ansible
	  ansible collection location = /home/ec2-user/.ansible/collections:/usr/share/ansible/collections
	  executable location = /home/ec2-user/.local/bin/ansible
	  python version = 3.6.8 (default, Aug 13 2020, 07:46:32) [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)]
	  jinja version = 3.0.1
	  libyaml = True
 
ansible --version | grep "python version"

#Install Python 3.8 + https://tecadmin.net/install-python-3-8-centos/

sudo yum -y install gcc openssl-devel bzip2-devel libffi-devel     - Step-4

pip3 install --user "pywinrm>=0.3.0"   - Step-5

pip3 install --user boto3              - Step-6


###Install Ansible collection for core Windows plugins using following command 
      
	"ansible-galaxy collection install ansible.windows"
	
			OR 
    Doenload "ansible-windows-1.7.2.tar.gz" tarball file from https://galaxy.ansible.com/ansible/windows 
	   and Install using following command.

    "$ansible-galaxy collection install ansible-windows-1.7.2.tar.gz"
	
	

Attach IAM policy to get accesss of EC2 target host machines In case of Dynamic Inventory.



Create new hosts.yml or add following entries in existing hosts file:
/**** hosts.yml *******************************
all:
  hosts:
    localhost:
  children:
    windowserver:
       hosts:
         10.10.10.10:
            ansible_user: ansible
            ansible_password: user@password
            ansible_connection: winrm
            ansible_winrm_transport: basic
            ansible_winrm_port: 5985
            ansible_winrm_server_cert_validation: ignore
			
/**** hosts.yml *******************************	

After completing all the setup execute following ansible command to test the connectivity with window host machine:

  "$ ansible windowserver -i hosts.yml -m win_ping"	
  

############## On Windows Machine:
##Some useful PS commands: 

Get-ChildItem -Path 'Cert:\LocalMachine\Root' | Where-Object {$_.Subject -Match "^CN=localhost.domain.com*"}

winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm enumerate winrm/config/Listener

winrm get winrm/config/Service

winrm get winrm/config/Winrs

# Update WinRM service configs :

#Service *Required
winrm get winrm/config/service
winrm get WinRM/Config/service/Auth

winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set WinRM/Config/service/Auth '@{Basic="true"}'
 
 
##Client Optional
winrm set winrm/config/client/auth @{Basic="true"} 
         
		OR
winrm set WinRM/Config/service/Auth
 '@{Basic="true";Kerberos="false";Negotiate="false";Certificate="false";CredSSP="false"}'


#If above two are set to false you will get following error :

	fatal: [10.198.169.5]: UNREACHABLE! => {"changed": false, "msg": "basic: the specified credentials were rejected by the server", "unreachable": true}

## To remove a WinRM listener:  If required

# Remove all listeners
   Remove-Item -Path WSMan:\localhost\Listener\* -Recurse -Force

# Only remove listeners that are run over HTTPS
   Get-ChildItem -Path WSMan:\localhost\Listener | Where-Object { $_.Keys -contains "Transport=HTTPS" } | Remove-Item -Recurse -Force

# Remove all ClientCertificates
	Remove-Item -Path WSMan:\localhost\ClientCertificate\* -Recurse -Force

################################################################################

Enable / Open ports 5985 and 5986 at window firewall level or network WAF level.


###### Enable Certificate Authentication ################

### https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html#generate-a-certificate

##Ansible Controller side OPENSSL Self Signed cert generation:
cat > openssl.conf << EOL
distinguished_name = req_distinguished_name
[req_distinguished_name]
[v3_req_client]
extendedKeyUsage = clientAuth
subjectAltName = otherName:1.3.6.1.4.1.311.20.2.3;UTF8:ansible@localhost
EOL
	
export OPENSSL_CONF=openssl.conf

openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -out ansible_cert.pem -outform PEM -keyout ansible_key.pem -subj "/CN=ansible" -extensions v3_req_client
	
rm openssl.conf 


##### Convert .jks certificate to .cert format. ##################################

#keystore.jks cert password: pass!


keytool -export -alias cert-name -file keystore.der -keystore keystore.jks

keytool -export -alias cert-name -file keystore.der -keystore keystore.jks

openssl x509 -inform der -in keystore.der -out keystore.crt
#########################################################################	

Create new hosts.yml or add following entries in existing hosts file:
/**** cert-auth-hosts.yml *******************************	
all:
  hosts:
    localhost:
  children:
    windowserver:
       hosts:
         10.10.10.10:
            ansible_user: ansible          
            ansible_connection: winrm          
            ansible_winrm_port: 5986
            ansible_winrm_server_cert_validation: ignore
            ansible_winrm_cert_pem: /opt/ansible/ansible_cert.pem
            ansible_winrm_cert_key_pem: /opt/ansible/ansible_key.pem
            ansible_winrm_transport: certificate
            ansible_winrm_scheme: https
/**** cert-auth-hosts.yml *******************************
	
	Execute below command to test the connectivity once you done with all the WinRM related configurations.
	
	"$ ansible windowserver -i cert-auth-hosts.yml -m win_ping"
	
	
#####################	

### WinRM side Configurations:

Step 1: Create ansible user manually and given him an administrator role .
Step 2: Execute the Powershell scripts provided in the following sequence:
     Download the required PS scripts from https://github.com/sandipsable111/ansible-winrm-cert-auth  
        1. enable_winrm.ps1 
		             - Script will not work you need to manually edit Local Group Policy 
		               Administrative Templates-> Windows Components - > Windows Remote Management (WinRM) -> WinRM Service - > edit "Allow remote server management through WinRM" and enable it, and enter the "*" as a values for IPv4 & IPv6 Filter.			 
		2. import_client_cert.ps1 - Copied from ansible machine creatd for ansible 
		                            user ansible_cert.pem (Public key) 
		3. create_ansible_user.ps1
		4. create_winrm_listener.ps1
		5. update_firewall.ps1
		
  Note: We can change listening HTTPS and HTTP ports from default to any other refer below links :
        https://adamtheautomator.com/winrm-port/

## Thats it and you are all set ############################


________________  END ____________________________________________________________		
	
### For references: ##################################

# https://adamtheautomator.com/ansible-winrm/

Set-Service -Name "WinRM" -StartupType Automatic
Start-Service -Name "WinRM"

if (-not (Get-PSSessionConfiguration) -or (-not (Get-ChildItem WSMan:\localhost\Listener))) {
    ## Use SkipNetworkProfileCheck to make available even on Windows Firewall public profiles
    ## Use Force to not be prompted if we're sure or not.
    Enable-PSRemoting -SkipNetworkProfileCheck -Force
}

Execute Following Script : 
## https://geekflare.com/connecting-windows-ansible-from-ubuntu/

https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1


	
    winrm set winrm/config/service '@{AllowUnencrypted="false"}'
	winrm set winrm/config/service/auth '@{Basic="false"}'
	winrm set winrm/config/service/auth '@{Negotiate="true"}'
	winrm set WinRM/Config/Client/Auth '@{Basic="false";Digest="false";Kerberos="false";Negotiate="true";Certificate="true";CredSSP="false"}'

## Issue Faced :
    Never set Negotiate="false" for /server/auth winrm confguration , it restricts you from accessing winrm service.
	
	Resolution: Computer > Policies > Administrative Templates > Windows Components > Windows Remote Management > WinRM Service:
		  Disallow Negotiate Authentication: Disabled	
####	
	
	#http://www.hurryupandwait.io/blog/certificate-password-less-based-authentication-in-winrm

	#Enable certificate authentication
		Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true
		
	$file = "C:\Ansible\cert-based-winrm-auth.ps1"
	powershell.exe -ExecutionPolicy ByPass -File $file		
 
 
    # Ansible side host variable configuration
	#https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html#certificate
	
		ansible_connection: winrm
		ansible_winrm_cert_pem: /path/to/certificate/public/key.pem
		ansible_winrm_cert_key_pem: /path/to/certificate/private/key.pem
		ansible_winrm_transport: certificate
