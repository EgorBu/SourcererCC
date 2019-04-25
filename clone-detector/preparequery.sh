#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
num_nodes="${1:-0}"
rootPATH=$(dirname $scriptPATH)
printf "\e[32m[preparequery.sh] \e[0mrootpath is : $rootPATH\n"
for i in $(seq 1 1 $num_nodes)
do
  foldername="$rootPATH/NODE_$i/query/"
  rm -rf $foldername
  mkdir -p $foldername
  queryfile="$rootPATH/query_$i.file"
  mv $queryfile $foldername/
  cp $rootPATH/sourcerer-cc.properties "$rootPATH/NODE_"$i/
  cp $rootPATH/res/log4j2.xml "$rootPATH/NODE"_$i/
done
