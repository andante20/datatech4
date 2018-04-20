#!/bin/bash

start=`date +"%Y-%m-%d" -d "$1"`
end=`date +"%Y-%m-%d" -d "-1 day"`

while [ "$start" != "$end" ] ; 
do 
        echo $start
        scrapy crawl woori --set FLUME_URL=http://dn01:50002 -s FEED_FORMAT=json --set START=$start --logfile /home/log/data2/$start.log
#        scrapy crawl woori --set FEED_URI=woori_2013.json --set FEED_FORMAT=json --set START=$start
        start=`date +"%Y-%m-%d" -d "$start + 1 day"`; 
done;
