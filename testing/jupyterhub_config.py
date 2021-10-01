"""sample jupyterhub config file for testing

configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""

c = get_config()  # noqa

from bioturingauth.auth import BioTuringAuthenticator

c.JupyterHub.authenticator_class = BioTuringAuthenticator

# docker testing only
#c.ConfigurableHTTPProxy.should_start = False

# Optionally set a global password that all users must use
# c.DummyAuthenticator.password = "your_password"

from jupyterhub.spawner import SimpleLocalProcessSpawner


c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

c.Spawner.args = ['--NotebookApp.allow_origin=*']
c.JupyterHub.redirect_to_server = False
c.JupyterHub.allow_named_servers = True
c.JupyterHub.tornado_settings = {
            'headers': {
                'Access-Control-Allow-Origin': "*",
                'Access-Control-Allow-Credentials': 'true'
                },
            }

c.ConfigurableHTTPProxy.auth_token = "Duytan@94"
c.ConfigurableHTTPProxy.extra_routes = {
    "/jupyterhub/sso/":"http://127.0.0.1:3000/jupyterhub/sso"
}
c.JupyterHub.base_url = "/jupyterhub"
c.JupyterHub.ssl_key = '/mnt/hdd3/tan/code/jupyterhub/key.key'
c.JupyterHub.ssl_cert = '/mnt/hdd3/tan/code/jupyterhub/key.crt'
