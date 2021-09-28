#!/bin/bash 
kubectl delete cm jupyterhub-config
kubectl create configmap --namespace default jupyterhub-config --from-file jupyterhub_config.py --dry-run -o yaml  | kubectl apply -f -
