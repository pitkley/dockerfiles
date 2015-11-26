#!/bin/sh

set -e

[ -f /var/lib/samba/.setup ] || {
    >&2 echo "[ERROR] Samba is not setup yet, which should happen automatically. Look for errors!"
    exit 127
}

samba -i -s /var/lib/samba/private/smb.conf
