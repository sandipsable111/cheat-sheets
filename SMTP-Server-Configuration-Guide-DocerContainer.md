# SMTP Server As A Docker Container (namshi/smtp)


This is a SMTP docker container for sending emails. You can also relay emails to gmail and amazon SES.

* [SMTP Docker Image (namshi/smtp)](https://hub.docker.com/r/namshi/smtp)

## Contents

1. [Configurations](#configurations)
   * [As A SMTP Server](#as-a-smtp-server)
   * [Docker Compose](#docker-compose)
   * [Start SMTP Container](#start-smtp-container)
   * [Configuration at Elasticsearch](#configuration-at-elasticsearch)

## Configurations
   Here we are configuring this SMTP docker container for sending email's directly to the user
   without using any other relay SMTP server like gmail and amazon SES.

### As A SMTP Server

* So to run this docker container as a SMTP Server, You don't need to specify any environment variable to get this up.
* You can pull the docker image with the help of below command

```console
$ docker pull namshi/smtp
```

### Docker Compose

You can create docker-compose file with below details:

docker-compose.yml

```console
version: '3.2'

services:
  smtp:
    image: namshi/smtp
    container_name: smtp_server
    restart: always
    ports:
     - "2525:25"  #exposing 2525 as a host port and 25 as a docker container port.
    networks:
     - default
	#You Need to configure below things if you want to use this container as a realy smtp server. 
    # environment:
     # # MUST start with : e.g RELAY_NETWORKS=:192.168.0.0/24:10.0.0.0/16
     # # if acting as a relay this or RELAY_DOMAINS must be filled out or incoming mail will be rejected
     # - RELAY_NETWORKS= :192.168.0.0/24
     # # what domains should be accepted to forward to lower distance MX server.
     # - RELAY_DOMAINS= <domain1> : <domain2> : <domain3>
     # # To act as a Gmail relay
     # - GMAIL_USER=
     # - GMAIL_PASSWORD=
     # # For use with Amazon SES relay
     # - SES_USER=
     # - SES_PASSWORD=
     # - SES_REGION=
     # # if provided will enable TLS support
     # - KEY_PATH=
     # - CERTIFICATE_PATH=
     # # the outgoing mail hostname
     # - MAILNAME=
     # # set this to any value to disable ipv6
     # - DISABLE_IPV6=
     # # Generic SMTP Relay
     # - SMARTHOST_ADDRESS=
     # - SMARTHOST_PORT=
     # - SMARTHOST_USER=
     # - SMARTHOST_PASSWORD=
     # - SMARTHOST_ALIASES=
```

### Start SMTP Container

Execute below command in the same directory where you have your docker-compose.yml file.

```console
$ docker-compose up
```
And after successful execution of above command your SMTP server will be up and ready to use.

###Configuration at Elasticsearch

Update elasticsearch configuration file config/elasticsearch.yml with below entries 

```console
xpack.notification.email.account:
  work:
    email_defaults:
      from: 'Watcher Alert <noreply@watcherAlertFiserv.com>'
    smtp:
      auth: false
      starttls.enable: false # Whether emails are sent encapsulated in TLS, or not.
      host: 10.1.0.22  #Host machine IP /DNS name where your SMTP docker container is running 
      port: 2525       #Port Exposed for host machine refer docker-compose.yml file of SMTP docker container
      user: alert@example.com  
      # password: fiserv@123  # Optional , IF you want to configure this field you should use a ealstic keyVault store to  
	  # store the password / secrets and fetch the value from there. Otherwise you will get an error for this field.
	  
#Use below in case of we have more than one email configuration
#xpack.notification.email:
    #  default_account: team1
    #  account:
    #    team1:
    #      ...
    #    team2:
    #      ...


xpack.notification.email.html.sanitization:
    allow: _tables, _blocks
    disallow: h4, h5, h6
```
