#!/bin/bash

start=`date +"%Y-%m-%d" -d "$1"`
end=`date +"%Y-%m-%d" -d "-1 day"`

while [ "$start" != "$end" ] ; 
do 
        echo $start
        scrapy crawl cauca_day --set FLUME_URL=http://dn01:50001 --set FEED_FORMAT=json --set START=$start -s END=$start --logfile /home/log/data1/$start.log
        start=`date +"%Y-%m-%d" -d "$start + 1 day"`; 
done;
