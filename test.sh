#!/bin/bash
export AUTH_SECRET="7ca688b260b4689286b8a4df8c1d96ee"
nvm use v12.12
jupyterhub -f testing/jupyterhub_config.py
