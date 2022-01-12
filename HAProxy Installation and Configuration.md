




HAProxy Installation and Configuration
On
 Ubuntu 18.4



Installing HAProxy
Use the apt-get command to install HAProxy.
$ sudo apt-get install haproxy

We need to enable HAProxy to be started by the init script.
$ sudo vi /etc/default/haproxy

Set the ENABLED option to 1
$ ENABLED=1

To check if this change is done properly execute the init script of HAProxy without any parameters. You should see the following.
$ service haproxy
Usage: /etc/init.d/haproxy {start|stop|reload|restart|status}




Preparing HAProxy
Here below are the sample postgresql nodes IP address considered while configuring HA proxy:
	Master Node: 		10.0.0.1
	First Slave Node: 		10.0.0.2
	Second Slave Node: 	10.0.0.3
We are going to have two ports open in haproxy for connection.
1.	Port 5000 for Primary Connections (Read-Write)
2.	Port 5001 for Standby Connections (Read-Only)
Here is the sample haproxy configuration (/etc/haproxy/haproxy.cfg) 
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
    bind *:7000  # on this port you can see HA-proxy UI in browser
    stats enable
    stats uri /

listen pgReadWrite
    bind *:5000
    option pgsql-check user primaryuser
    default-server inter 3s fall 3
    balance     roundrobin
    server master 10.0.0.1:5432 check port 5432
    server slave1   10.0.02:5432 check port 5432
    server slave2   10.0.0.3:5432 check port 5432

listen pgReadOnly
    bind *:5001
    option pgsql-check user standbyuser
    default-server inter 3s fall 3
    balance     roundrobin
    server master 10.0.0.1:5432 check port 5432
    server slave1   10.0.02:5432 check port 5432
    server slave2   10.0.0.3:5432 check port 5432

Once we have the configuration ready, the haproxy service can be started up
$ sudo systemctl start haproxy OR $ sudo service haproxy start
At this stage, all nodes will be listed as candidates for both read-write and read-only connections which will be marked in the green background color.

To access HA-Proxy UI hit the URL     http://{haproxyserver-IP}:7000
You can see the UI like shown in the below sample UI screen snap:
 



To Configure databse using HA Proxy URL you can use below details:
Database Configuration URL’s:
-	DB URL: {haproxyserver-IP}:5000   OR     {haproxyserver-IP}:5001 
-	DB USER NAME: Database username that you have created.
-	DB password : Password of the above DB user
