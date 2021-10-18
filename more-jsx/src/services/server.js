const axios = require('axios');

const {getAPIUrl} = require("./utils");

const spawnNewserver = function(user, servername, profile) {
	const encodedServerName = encodeURIComponent(servername);
	const endpoint = `spawn/${user}/${encodedServerName}`;
	var bodyFormData = new FormData();
	bodyFormData.append('profile', profile)
	return axios.post(getAPIUrl(endpoint), bodyFormData)
}

const getSpawningProgressURL = function(user, servername) {
	const encodedServerName = encodeURIComponent(servername);
	console.log("username:", user, "servername:", encodedServerName);
	const endpoint = `api/users/${user}/servers/${encodedServerName}/progress`;
	return getAPIUrl(endpoint);
}

module.exports = {
	spawnNewserver,
	getSpawningProgressURL
}