#!/bin/bash
set -e

if [[ "$1" != "/"* ]]; then
    exec journalbeat "$@"
fi

exec "$@"

