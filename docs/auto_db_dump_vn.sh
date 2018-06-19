#!/bin/bash
# variables
path=/tmp/vn_dumps/
filenew=backup_$(date +"%d%m%Y").sql.gz
fileold=backup_$(date -d "yesterday" +"%d%m%Y").sql.gz
subject="Visual novel DB dump"
body="Dump was created today."
addresses="haron2012@mail.ru dolamroth@mail.ru"
# addresses split by space. support only mail.ru domain

# create dir if not exist
mkdir -p $path

# check that newfile not exist (if exit)
if [ -f $path$filenew ]; then
    echo "Today's dumpfile exists"
    exit 1
fi

# delete previous dump
if [ -f $path$fileold ]; then
    rm $path$fileold
fi

# create new dump
pg_dumpall -U postgres | gzip > $path$filenew

# sending emails to recipients list
echo $body | mail -s "$subject" -a $path$filenew "$addresses"
