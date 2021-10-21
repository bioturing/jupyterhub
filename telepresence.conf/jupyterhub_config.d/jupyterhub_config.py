"""sample jupyterhub config file for testing

configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""


#from bioturingauth.auth import BioTuringAuthenticator

c.JupyterHub.authenticator_class = 'bioturingauth.auth.BioTuringAuthenticator'
c.Authenticator.admin_users = {'tan@bioturing.com'}


# Optionally set a global password that all users must use
# c.DummyAuthenticator.password = "your_password"

#from jupyterhub.spawner import SimpleLocalProcessSpawner

#c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

c.BioTuringKubeSpawner.profile_list = [
                {
                    'display_name': 'Datascience notebook - Small Instance',
                    'slug': 'datascience-small',
                    'default': True,
                    'kubespawner_override': {
                        'image': 'k8s-notebook:latest',
                        'cpu_limit': 2,
                        'mem_limit': '4G',
                    }
                },
				{
                    'display_name': 'Datascience notebook - Medium Instance',
                    'slug': 'datascience-medium',
                    'kubespawner_override': {
                        'image': 'k8s-notebook:latest',
                        'cpu_limit': 4,
                        'mem_limit': '8G',
                    }
                },
				{
                    'display_name': 'Datascience notebook - Large Instance',
                    'slug': 'datascience-large',
                    'kubespawner_override': {
                        'image': 'k8s-notebook:latest',
                        'cpu_limit': 8,
                        'mem_limit': '16G',
                    }
                },
                {
                    'display_name': 'Single-cell notebook CellChat - Medium Instance',
                    'slug': 'singlecell-cellchat',
                    'kubespawner_override': {
                        'image': 'k8s-notebook:latest',
                        'cpu_limit': 4,
                        'mem_limit': '8G',
                        }
                    }
                  
]
c.Spawner.args = ['--NotebookApp.allow_origin=*']
c.Spawner.default_url = '/tree'

c.JupyterHub.allow_named_servers = False
c.JupyterHub.tornado_settings = {
            'headers': {
                'Access-Control-Allow-Origin': "*",
                'Access-Control-Allow-Credentials': 'true'
                },
            }
c.ConfigurableHTTPProxy.extra_routes = {
    "/jupyterhub/sso/":"http://127.0.0.1:3000/jupyterhub/sso"
}
#c.JupyterHub.ssl_key = '/mnt/hdd3/tan/docs/k8s/jupyter-hub/JupyterHub-on-Kubernetes/images/jupyter-hub/jupyterhub/key.key'
#c.JupyterHub.ssl_cert = '/mnt/hdd3/tan/docs/k8s/jupyter-hub/JupyterHub-on-Kubernetes/images/jupyter-hub/jupyterhub/key.crt'
