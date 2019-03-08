#!/bin/bash

tableName=$1

/usr/bin/mysql -u root -ppassword -A -e "set @tableName=${tableName}; source test2.sql;"

exit
