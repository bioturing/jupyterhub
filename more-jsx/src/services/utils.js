const baseUrl = process.env.BASE_URL;

const hubPrefix = `${window.location.protocol}//${window.location.host}${baseUrl}`;
const getAPIUrl = function(endpoint) {
	return `${hubPrefix}hub/${endpoint}`
}

const getUserUrl = function(endpoint) {
	return `${hubPrefix}user/${endpoint}`
}

const getNotebookPendingEndpoint = function(user, provId) {
	return `wss://${window.location.host}${baseUrl}user/${user}/nbapi/provision-pending/${provId}`
}

const getNotebookUrl = function(user, nbFileName, prefix) {
	// TODO: add prefix
	return `${hubPrefix}user/${user}/notebooks/${nbFileName}`
}

const normalizeRoute = function(route) {
	return `${process.env.BASE_URL}hub/home${route}`;
}

module.exports = {
	getAPIUrl,
	getUserUrl,
	getNotebookPendingEndpoint,
	getNotebookUrl,
	normalizeRoute
}