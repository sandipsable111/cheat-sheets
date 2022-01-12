#Jenkins Installation to run AWS cloud formation templates:

sudo yum install java-1.8.0-openjdk-devel

yum install wget

sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo

sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

sudo yum install jenkins 

sudo service jenkins start

echo "Jenkins started on default port 8080 ..."

echo "Your Admin login password is below: "

cat cd /var/lib/jenkins/secrets/initialAdminPassword


####### Uninstall Jenkins 

sudo service jenkins stop


sudo yum remove jenkins

####################################################################


yum install zip unzip -y

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

unzip awscliv2.zip

sudo ./aws/install

echo "AWS CLI installation success ..."

aws --version



#Uninstall Java 
rpm -qa | grep java

rpm -qa | grep jdk

sudo yum remove jdk1.7.0  # use this 
or  
rpm -e jdk1.7.0 


