#!/bin/sh

RUN_EXIT=$1

if [ "$RUN_EXIT" -eq 127 ]; then
    sleep infinity
elif [ "$RUN_EXIT" -lt 0 ]; then
    exit 1
else
    exit "$RUN_EXIT"
fi
