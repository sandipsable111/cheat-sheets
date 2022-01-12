










How to Set-Up Master-Slave Replication for PostgreSQL 11 












Recommendation: I would recommend you that , Please  do not install PostgreSQL 10 I faced many issues with that version, So I must say,  you must go with PostgreSQL 11.
Step 1 – Install PostgreSQL 11
-	Import the PostgreSQL signing key to the system using below command
$ sudo apt-get install wget ca-certificates
$ sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'

-	Now update the system repository with apt command.
$ sudo apt update

-	Next, install the PosgreSQL 11 package with the apt command below.

	$ sudo apt-get install postgresql-11

-	If the installation has been completed, add it to start automatically at boot time
$ sudo systemctl enable postgresql

-	By default, PostgreSQL is running on the localhost (127.0.0.1) IP address with port 5432 on Ubuntu, check it with netstat command.
$ netstat -plntu | grep 5432
$ netstat -nlp | grep postgresql

-	PostgreSQL 11 is running on the system. In the next step, we have to configure a password for the postgres user
-	From the root account, log in to the postgres user with the su command, then access the postgres front-end terminal psql
$ sudo su - postgres
$ psql

-	Please change the password for the postgres user.
$ sudo \password postgres

-	PostgreSQL 11 has been installed on the system, is running without error and the password for postgres user has been updated.
-	Repeat the same for another servers (Slaves and Master).








Step 2 – Configure the PostgreSQL MASTER Server


-	The master server has the IP address 15.0.10.M, and the postgres service will run under that IP with default port. The master server will have permission for the READ and WRITE to the database and perform streaming replication to the slave server.
-	Go to the postgres configuration directory ‘/etc/postgresql/11/main‘ and edit the postgresql.conf file with vim / nano editor.
$ cd /etc/postgresql/11/main/
$ vi postgresql.conf

-	Uncomment ‘listen_addresses’ line and change the value to the  ‘*’  so it will be available for all to access/ connect to that DB server.
listen_addresses = '*'

-	Uncomment ‘wal_level’ line and change value to the ‘ replica‘
wal_level = replica

-	wal_level determines how much information is written to the WAL. The default value is replica, which writes enough data to support WAL archiving and replication, including running read-only queries on a standby server. minimal removes all logging except the information required to recover from a crash or immediate shutdown. Finally, logical adds information necessary to support logical decoding. Each level includes the information logged at all lower levels. This parameter can only be set at server start.
In releases prior to 9.6, this parameter also allowed the values archive and hot_standby. These are still accepted but mapped to replica.
-	For the synchronization level, we will use local sync. Uncomment and change value line as below
synchronous_commit = local

-	Enable archiving mode and change the archive_command option to the command ‘cp %p /var/lib/postgresql/11/main/archive/%f’.
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/11/main/archive/%f'

-	For the ‘Replication’ settings, here we are using 3 servers one master and 2 slaves, uncomment the ‘wal_sender‘ line and change value to 3, and for the ‘wal_keep_segments‘ value is 10.
max_wal_senders = 3
wal_keep_segments = 10
-	For the application name, uncomment ‘synchronous_standby_names’ line and change the value to the name ‘pgslave001, pgslave002’ 
synchronous_standby_names = 'pgslave001, 'pgslave002'

-	Save the file and exit the editor
-	In the postgresql.conf file, the archive mode is enabled, so we need to create a new directory for the archive. Create a new archive directory, change the permission and change the owner to the postgres user.
$ sudo mkdir -p /var/lib/postgresql/11/main/archive/
$ sudo chmod 700 /var/lib/postgresql/11/main/archive/
$ sudo chown -R postgres:postgres /var/lib/postgresql/11/main/archive/

-	Next, edit pg_hba.conf file for authentication configuration.
$ sudo vi pg_hba.conf

-	Paste configuration below to the end of the line.
#allow clients to connect to this DB server
host    all     all          0.0.0.0/0            md5
# PostgreSQL Master IP address
host    replication     replica          15.0.10.M/32            md5
# PostgreSQL Slave IP address
host    replication     replica          15.*.*.*/32            md5
host    replication     replica          15.0.99.**/32            md5

-	Save and exit, then restart PostgreSQL.
$ sudo systemctl restart postgresql

-	PostgreSQL is running under the IP address 15.0.10.M, check it with netstat command.
$ netstat -plntu

-	Next, create a new user for replication. We will create a new user named ‘replica‘ with password ‘password ‘. Please choose a secure password here for your setup! Log in to the postgres user and access the postgres front-end terminal psql.
$ sudo su - postgres
$ psql

-	Create new ‘replica‘ user with password ‘aqwe123@‘ with postgres query below.
$ CREATE USER replica REPLICATION LOGIN ENCRYPTED PASSWORD 'password';
-	Now check the new user with ‘du‘ query below, and you will see the replica user with replication privileges.
$ \du

-	MASTER server configuration has been completed.


Step 3 – Configure SLAVE Server

-	Repeat the below steps for all the slave servers
-	The SLAVE server has IP address 15.0.10.S1 and 15.0.10.S2 And these servers will only have a READ permission to the database. The Postgres database server will run under the IP address of the server, not a localhost IP
-	Stop the postgres service on the slave server with the systemctl command below.
$ systemctl stop postgresql OR $ sudo service postgresql stop

-	Go to the Postgres configuration directory ‘/etc/postgresql/11/main‘, then edit the configuration file ‘postgresql.conf‘.
$ cd /etc/postgresql/11/main/
$ sudo vi  postgresql.conf

-	Refer master servers postgresql.conf file configuration steps and do the same configuration for the slave server
-	Slave server requires one additional configuration - Enable hot_standby for the slave server by uncommenting the following line and change value to ‘on‘.
hot_standby = on

-	Save the file and exit the editor.













Step 4 – Copy PostgreSQL Data from the MASTER to the SLAVE
-	Next, we want to replace the postgres main directory on the ‘SLAVE‘ server with the main data directory from ‘MASTER‘ server.
-	Log in to the SLAVE server and access postgres user.
su – postgres

-	Go to the postgres data directory ‘main‘ and backup it by renaming the directory name.
$ cd /var/lib/postgresql/11/
$ mv main main-backup-01

-	Create new ‘main‘ directory as ‘postgres‘ user and make sure have a permission like the main-backup-01 directory
$ mkdir main/
$ chmod 700 main/

-	Next, copy the main directory from the MASTER server to the SLAVE server with pg_basebackup command, we will use replica user to perform this data copy.
$ pg_basebackup -h 15.0.10.M -U replica -D /var/lib/postgresql/11/main -P

-	When the data transfer is complete, go to the main data directory and create a new recovery.conf file.
$ cd /var/lib/postgresql/11/main/
$ vi recovery.conf

-	Paste the configuration below:
standby_mode = 'on'
primary_conninfo = 'host=15.0.10.M port=5432 user=replica password=password 
# pgslave001- for slave1, pgslave002- for Slave2
application_name=pgslave001'
restore_command = 'cp /var/lib/postgresql/11/main/archive/%f %p'
trigger_file = '/tmp/postgresql.trigger.5432'


-	Save and exit, then change the permissions of the file to 600 with chmod.
$ chmod 600 recovery.conf

-	Now exit from postgres user and start PostgreSQL 11 on the SLAVE server and make sure the postgres service is running on IP address 15.0.10.S1 with netstat.
$ exit
$ systemctl start postgresql OR $ sudo service postgresql start
$ netstat -plntu


-	Data transfer and configuration for the SLAVE server has been completed.

Step 5 – Testing.

-	Configure the master and slave servers in pgAdmin 
-	Test with different scenarios
-	Perform DB operations on master database and observe all Slave database.
-	Whatever changes done on master server should replicate on all the slaves. 


Limitations:
-	Can’t easily scale to handle growth i.e. we can’t add slaves dynamically.
-	If we want to add slaves, we need to update the master node configuration and need to restart that node to consider those newly added slaves.























Sample pg_hba.conf file enries for master:

# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
host    all             all             10.0.0.0/32             md5
host    all             all             0.0.0.0/0               md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     replica         127.0.0.1/32            md5
host    replication     all             ::1/128                 md5

# This is your master CIDR/IP
host    replication     replica              10.0.0./32          md5
# This is your slave CIDR/IP
host    replication     replica              10.0.0./32          md5
host    replication     replica              10.0.0./32           md5
