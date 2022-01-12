User: postgres /Password


Postgresql 10 Installation:

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

sudo apt update
sudo apt install postgresql postgresql-contrib


Ver Cluster Port Status Owner    Data directory              Log file
10  main    5432 down   postgres /var/lib/postgresql/10/main /var/log/postgresql/postgresql-10-main.log


Install Postgresql 11 on Ubuntu:

sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'

	$ sudo apt update

	$ sudo apt-get install postgresql-11

	$ sudo systemctl stop postgresql.service
	$ sudo systemctl start postgresql.service
	$ sudo systemctl enable postgresql.service
	$ sudo systemctl status postgresql.service

To see the service is listening on which port: 
	$ netstat -nlp | grep postgres 

sudo passwd postgres
sudo su -l postgres
psql
postgres=# \password

https://websiteforstudents.com/how-to-install-postgresql-11-on-ubuntu-16-04-18-04-servers/

Ver Cluster Port Status Owner    Data directory              Log file
11  main    5432 down   postgres /var/lib/postgresql/11/main /var/log/postgresql/postgresql-11-main.log


Installed Telnet :
Chek slaves are able to access master on port 5432 using below command

telnet masters-ip 5432


If you got an error like- "telnet: Unable to connect to remote host: Connection refused"

- Kindly go and update the postgresql.conf file at "/etc/postgresql/10/main"
- update the value of listen_addresses with 
	"your IP" address for allowing perticular IP to access this DB
  OR "*" / "0.0.0.0"  - To allow everyone to access this DB
  
  Example: listen_addresses = '0.0.0.0'  / listen_addresses = '*' / listen_addresses = '10.25.65.10'
  
- Restart postgresql service using bleow command
	$ sudo service postgresql restart
	
-List all the runnig services:
	$ sudo service --status-all | grep postgresql
	
	
- Check connection now: $ telnet masters-ip 5432

IF telnet is not installed on your system follwo the below steps:

			(https://stackoverflow.com/questions/34389620/telnet-unable-to-connect-to-remote-host-connection-refused)
			sudo apt-get install xinetd telnetd

			update / Edit /etc/xinetd.conf in main OS,make its content look like following 

			Simple configuration file for xinetd
			#
			# Some defaults, and include /etc/xinetd.d/
			defaults
			{
			# Please note that you need a log_type line to be able to use log_on_success
			# and log_on_failure. The default is the following :
			# log_type = SYSLOG daemon info
			instances = 60
			log_type = SYSLOG authpriv
			log_on_success = HOST PID
			log_on_failure = HOST
			cps = 25 30
			}

			Restart Service : sudo /etc/init.d/xinetd restart 
			
Master Slave Configuration:

https://www.rsupernova.com/how-to-set-up-master-slave-replication-for-postgresql-11-on-ubuntu-18-04/




Uninstall:

sudo service postgresql stop

sudo apt-get --purge remove postgresql\*


dpkg -l | grep postgres

Will get you the list of those packages that Postgres installed. Then, just use the same "apt-get --purge remove ...." command but instead of just postgresql, type each package name, separated by spaces, like:

sudo apt-get --purge remove postgresql postgresql-doc postgresql-common

sudo apt-get --purge remove pgdg-keyring





In the slave Configuration:

pg_basebackup -h 10.0.0.159 -D /var/lib/postgresql/11/main/ -P -U postgres --wal-method=stream




Update file pg_hbg.conf

# This is your master CIDR/IP 
host replication replication 10.0.0.159/32 md5 
# This is your slave CIDR/IP 
host replication replication 10.0.0.237/32 md5 


wal_level = hot_standby
max_wal_senders = 5  # Recommended to allocate 5 per slave 
hot_standby = on 
wal_keep_segments = 1000    # Each segment is 16Megs.  


# on master 
archive_mode = on 
archive_command = 'cp %p /path_to/archive/%f'   

# on slave 
restore_command = 'cp /path_to/archive/%f "%p"'  






