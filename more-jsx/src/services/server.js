const axios = require('axios');

const {getAPIUrl, getUserUrl} = require("./utils");

const spawnNewserver = function(user) {
	const endpoint = `spawn/${user}`
	return axios.post(getAPIUrl(endpoint))
}

const getSpawningProgressURL = function(user, servername) {
	const endpoint = `api/users/${user}/server/progress`;
	return getAPIUrl(endpoint);
}

const spawnNotebook = function(user, nb_id) {
	const endpoint = `${user}/nbapi/provision`;
	return axios.post(getUserUrl(endpoint), null, {params: {
		nb_id
	}})
}

module.exports = {
	spawnNewserver,
	getSpawningProgressURL,
	spawnNotebook
}