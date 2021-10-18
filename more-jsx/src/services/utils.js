const baseUrl = process.env.BASE_URL;

const getAPIUrl = function(endpoint) {
	return `${window.location.protocol}//${window.location.host}${baseUrl}hub/${endpoint}`
}

module.exports = {
	getAPIUrl: getAPIUrl
}