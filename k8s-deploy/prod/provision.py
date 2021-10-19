import os
import requests
import base64

def get_groups():
	username = os.environ["JUPYTERHUB_USER"]
	admin_service = os.environ["BESP_ADMIN_SERVICE"]
	admin_password = os.environ["BESP_ADMIN_PASSWORD"]
	b64pass_bytes = admin_password.encode('ascii')
	b64pass = base64.b64encode(b64pass_bytes)

	# create a session object
	s = requests.Session()
	res = s.post("http://{admin_service}/auth/login".format(admin_service=admin_service), 
		data={"username" : "admin", "password": b64pass})
	res_d = res.json()
	token = res_d["token"]
	s.headers.update({"Authorization": token})
	res_groups = s.get("http://{admin_service}/user/{username}/getGroups".format(
		admin_service=admin_service,
		username=username
		))
	groups = res_groups.json()["groups"]
	return [g["GroupName"] for g in groups]

def provision():
	def norm_path(path):
		return path.replace('/','\\').replace(' ','\ ')
	groups = get_groups()
	basedir_private = os.path.join([os.environ["BESP_DIR"], 
			"private_studies_path"])
	user_studies_path = os.path.join([os.environ["BESP_DIR"], 
			"private_user_studies_path",
			os.environ["JUPYTERHUB_USER"]])
	group_studies_path = [norm_path("{basedir}/{group}") for g in groups]
	lowerdir = ":".join([user_studies_path] + group_studies_path)
	upperdir =  "/data/upper"
	workdir = "/data/work"
	
if __name__ == "__main__":
	provision()