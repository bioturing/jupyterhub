#!/bin/bash
set -a
source <(cat telepresence.env | \
    sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
set +a
jupyterhub --config $TELEPRESENCE_ROOT/usr/local/etc/jupyterhub/jupyterhub_config.py 
