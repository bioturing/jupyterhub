# Build jupyterhub image for k8s deployment

This command will build the image for the `hub` component. It includes the `bioturingauth` python package for authentication and the main `jupyterhub` repo
Some requirements are copied from the repo `zero-to-jupyterhub-k8s` for kubernetes deployment
```bash
docker build -t k8s-jupyterhub -f Dockerfile-k8s .
```

# Build `auth-proxy` image for sso authentication 

The `auth-proxy` image will be deployed in the same pod with the `configurable-http-proxy`.
We change the default login route of jupyterhub to `/<baseurl>/sso`. The `auth-proxy` container
will wait for a hook from `bioturing.com` to post a hook back to the client. Then we create a POST request 
to `jupyterhub` to log the user in. `Jupyterhub` will be responsible for the redirect afterwards

```bash
cd  bioturingauth
docker build -t auth-proxy .
```
