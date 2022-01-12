HA PROXY INSTALLATIOn 


global
    maxconn 100

defaults
    log global
    mode tcp
    retries 2
    timeout client 30m
    timeout connect 4s
    timeout server 30m
    timeout check 5s

listen stats
    mode http
    bind *:7000
    stats enable
    stats uri /

listen pgReadWrite
    bind *:5000
    option pgsql-check user primaryuser
    default-server inter 3s fall 3
	balance     roundrobin
    server master 10.0.0.1:5432 check port 5432
    #server slave1 10.0.0.2:5432 check port 5432
    #server slave2 10.0.0.3:5432  check port 5432

listen pgReadOnly
    bind *:5001
    option pgsql-check user standbyuser
    default-server inter 3s fall 3
	balance     roundrobin
    #server master 10.0.0.1:5432 check port 5432
    server slave1 10.0.0.2:5432 check port 5432
    server slave2 10.0.0.3:5432  check port 5432





Installing Patroni
Patroni is an open-source python package that manages Postgres configuration. It can be configured to handle tasks like replication, backups, and restorations. 

Patroni uses utilities that come installed with Postgres, located in the /usr/lib/postgresql/10/bin directory by default on Ubuntu 18.04. You will need to create symbolic links in the PATH to ensure that Patroni can find the utilities. 

Type below command to create a symbolic link and make sure you replace the postgresql version if you are running an earlier or later release.

sudo service postgresql stop
sudo ln -s /usr/lib/postgresql/10/bin/* /usr/sbin/


Type the below command to install python and python-pip packages:
sudo apt -y install python python-pip


Ensure that you have the latest version of the setuptools of python package with below command:
sudo -H pip install --upgrade setuptools

Install required dependencies:
sudo apt install libpq-dev


Type below command to install psycopg2:
sudo -H pip install psycopg2

sudo -H pip install patroni
sudo -H pip install python-etcd


Create below config file:

sudo nano /etc/patroni.yml

scope: postgres
namespace: /db/
name: slave1

restapi:
    listen: 10.0.0.7:8008
    connect_address: 10.0.0.7:8008

etcd:
    host: 10.0.0.7:2379

bootstrap:
    dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
        postgresql:
            use_pg_rewind: true

    initdb:
    - encoding: UTF8
    - data-checksums

    pg_hba:
    - host replication replicator 127.0.0.1/32 md5
    - host replication replicator 10.0.0.9/0 md5
    - host replication replicator 10.0.0.3/0 md5
    - host all all 0.0.0.0/0 md5

    users:
        postgres:
            password: pass
            options:
                - createrole
                - createdb

postgresql:
    listen: 10.0.0.7:5432
    connect_address: 10.0.0.7:5432
    data_dir: /data/patroni
    pgpass: /tmp/pgpass
    authentication:
