"""sample jupyterhub config file for testing

configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""


#from bioturingauth.auth import BioTuringAuthenticator

c.JupyterHub.authenticator_class = 'bioturingauth.auth.BioTuringAuthenticator'

c.Spawner.args = ['--NotebookApp.allow_origin=*']
c.Spawner.default_url = '/lab'
c.KubeSpawner.profile_list = [
			{
                    'display_name': 'Training Env - Datascience',
                    'slug': 'training-datascience',
                    'kubespawner_override': {
                        'image': 'jupyter/datascience-notebook:lab-3.1.11',
                        'cpu_limit': 4,
                        'mem_limit': '8G',
					}
			}
        ]
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
