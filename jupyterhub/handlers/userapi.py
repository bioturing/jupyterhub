import json

from tornado import web

from ..apihandlers.base import APIHandler

from .. import __version__
from ..scopes import needs_scope

class UserServerInfoAPIHandler(APIHandler):
	"""Get server info"""
	@web.authenticated
	@needs_scope("servers")
	async def get(self):
		user = self.current_user
		status = 404 if user == None else 200
		spawners = user.spawners.values()
		spawners_info = []
		for spawner in spawners:
			spawners_info.append(self.server_model(spawner))

		self.set_header('Content-Type', 'text/plain')
		self.set_status(status)
		self.write(json.dumps(spawners_info))

default_handlers = [
    (r'/userapi/server-info$', UserServerInfoAPIHandler),
]
