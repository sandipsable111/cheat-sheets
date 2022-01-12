#!/bin/bash -ex

# Importing PostgreSQL signing key
echo "Importing the PostgreSQL signing key to the system..."
sudo apt-get install wget ca-certificates
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'

# Ensures the server is up to date before proceeding.
echo "Updating server..."
sudo apt update


echo " "
echo " "
echo "Installing PostgreSQL..."
sudo apt-get install postgresql-11
echo "#########################################################################################"
echo "PostgreSQL Installation Is Successfull ..."
echo "#########################################################################################"


#Check is it running
echo " "
echo " "
echo "Checking is it running on default port 5432 ..."
netstat -plntu | grep 5432
netstat -nlp | grep postgresql
echo " "
echo " "

# Update/ Set password for default user 'postgres'
echo " "
echo " "
echo " "
echo " "
echo " "
echo "#########################################################################################"
echo " Please Follow the below mandatory steps.... "
echo "   "
echo "Please Update a password for the default postgres user by executing below commands sequentially:"
echo " "
echo " 1. psql "
echo " 2. \password postgres"
echo " 3. After updating password for postgres user just type '\q' or 'exit' to come out"
echo " 4. Now next step is you need to update two configuration files in order to access DB server from outside (Other than localhost server)"
echo "          1. postgresql.conf"
echo "          2. pg_hba.conf"
echo "  "
echo "#########################################################################################"

sudo su - postgres
