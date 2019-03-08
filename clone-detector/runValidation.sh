#!/bin/bash
 
## define an array ##
#arrayname=(cglib dom4j hibernate junit log4j lucene)
## get item count using ${arrayname[@]} ##
for project in $(ls /Users/vaibhavsaini/Dropbox/clonedetection/projects/)
do
  echo "running java -jar dist/validation.CloneBugPattern.jar $project"
  java -Xms13g -Xmx13g -jar dist/validation.CloneBugPattern.jar $project
done
