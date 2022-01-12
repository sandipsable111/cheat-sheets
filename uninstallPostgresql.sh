#!/bin/bash -ex
# Uninstalling postgresql

echo " Uninstalling Postgresql ..."
sudo service postgresql stop

sudo apt-get --purge remove postgresql\*

dpkg -l | grep postgres

sudo apt-get --purge remove pgdg-keyring


echo " Postgresql Successfully Uninstalled ..."
