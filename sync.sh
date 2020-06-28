#!/bin/bash

set -o xtrace -e -u -o pipefail -o posix

# A simple script to keep in sync one folder on local host with a remote host. I use it to keep my code synced with
# a RaspberryPi while I edit it on my desktop.
# 
# NOTE 1: make sure that you copy your keys to remote host with `ssh-copy-id` 
# first to allow for rsync to run without password prompts.
# NOTE 2: set the variables below to suit your needs.

LOCAL_DIR="Code"
REMOTE_HOST="192.168.0.54"
REMOTE_USERNAME="pi"
REMOTE_DIR="/home/pi/Documents/github/Freenove_Pi"

# Try first to sync to see if ssh is set up correctly.
rsync -v -y -r $LOCAL_DIR $REMOTE_USERNAME@$REMOTE_HOST:$REMOTE_DIR

while true; do
    inotifywait -r -e modify -e create -e delete -e move -e attrib $LOCAL_DIR
    rsync -v -y -r $LOCAL_DIR $REMOTE_USERNAME@$REMOTE_HOST:$REMOTE_DIR
done
