#!/bin/bash
sed -i '/^BASE_URL/d' .env
echo "BASE_URL=/jupyterhub/" >> .env
npm run-script build
npm run-script place
