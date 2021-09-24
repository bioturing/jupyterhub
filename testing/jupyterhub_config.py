"""sample jupyterhub config file for testing

configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""

c = get_config()  # noqa

from bioturingauth.auth import  DictionaryAuthenticator

c.JupyterHub.authenticator_class = DictionaryAuthenticator

# Optionally set a global password that all users must use
# c.DummyAuthenticator.password = "your_password"

from jupyterhub.spawner import SimpleLocalProcessSpawner

c.JupyterHub.spawner_class = SimpleLocalProcessSpawner
c.Spawner.args = ['--NotebookApp.allow_origin=*']
c.JupyterHub.tornado_settings = {
            'headers': {
                'Access-Control-Allow-Origin': "http://127.0.0.1:3000",
                'Access-Control-Allow-Credentials': 'true'
                },
            }
c.ConfigurableHTTPProxy.api_token = 'abc123'
#c.JupyterHub.ssl_key = '/mnt/hdd3/tan/docs/k8s/jupyter-hub/JupyterHub-on-Kubernetes/images/jupyter-hub/jupyterhub/key.key'
#c.JupyterHub.ssl_cert = '/mnt/hdd3/tan/docs/k8s/jupyter-hub/JupyterHub-on-Kubernetes/images/jupyter-hub/jupyterhub/key.crt'
