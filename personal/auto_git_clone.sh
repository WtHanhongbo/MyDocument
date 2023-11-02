#!/bin/bash

if [ $# != 2 ]; then
    echo "Too many or too few parameters!!!  the count of parameters is: $#"
    echo "Please use the script as: ./auto_git_clone.sh [code path] \"[git command]\" "
    exit 1
fi

codePath=$1
cloneCommand=$2

echo "The code dir is: $codePath"
echo "The clone command is: $cloneCommand"

if [ ! -d $codePath ]; then
    echo "The dir $codePath does not exist, mkdir -p $codePath"
	mkdir -p $codePath
	
	if [ $? != 0 ]; then
	    echo "Error: mkdir failed!!! Exit"
	    exit 1
	fi
fi

cd $codePath
currentPath=`pwd`
echo "Current path is: $currentPath"

echo "==============start excute git command========="
$2
while [ $? != 0 ]; do
	echo "git clone failed, git clone again========"
	sleep 3
	$2
done


