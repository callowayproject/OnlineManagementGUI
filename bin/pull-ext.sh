#!/bin/bash
FILES=$VIRTUAL_ENV/src/*

for f in $FILES
do
    if [ -d $f ] 
    then
        cd $f
        if [ -e .git ] 
        then
            git pull origin master
        elif [ -e .bzr ] 
        then
            bzr merge
        elif [ -e .hg ]
        then
            hg pull
        elif [ -e .svn ]
        then
            svn up
        fi
    fi
done