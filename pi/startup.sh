#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR
/usr/bin/python3 -u $DIR/main.py 10 &> $DIR/oatmeal.log &
echo "Started Oatmeal"
exit 0
