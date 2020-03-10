#!/bin/bash

sudo systemctl stop serial-getty@ttyAMA0.service

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

cp $DIR/oatmeal.log $DIR/otameal.log.old
/usr/bin/python3 -u $DIR/main.py 10 &> $DIR/oatmeal.log &
echo "Started Oatmeal"

exit 0
