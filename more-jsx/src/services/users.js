const {getAPIUrl} = require("./utils");

const getWhoAmI = function() {
	return fetch(getAPIUrl("api/user"))
		.then(data => data.json())
}

const getPublicNotebooks = function() {
	return fetch(`${process.env.NOTEBOOK_PUBLIC_REPO}`)
		.then(data => data.json())
}

module.exports = {
	getWhoAmI,
	getPublicNotebooks
}