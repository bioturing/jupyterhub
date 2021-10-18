const {getAPIUrl} = require("./utils");

const getWhoAmI = function() {
	return fetch(getAPIUrl("api/user"))
		.then(data => data.json())
}

module.exports = {
	getWhoAmI : getWhoAmI,
}