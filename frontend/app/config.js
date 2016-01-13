'use strict';

/**
 * Created by caio on 13/01/16.
 */

var CONFIG = {
	/* Frontend server configuration */
	'hostname': '0.0.0.0',
	'port': 9000,
	'portDev': 9001,
	'portLivereload': 35729,

	/* Backend infos */
	'backendProtocol': 'http',
	'backendHostName': '0.0.0.0',
	'backendPort': '8000',
	'backendAPIPath':'/api/v1',

	'buildApiUri': function(path) {
		return CONFIG.backendProtocol +'://'+ CONFIG.backendHostName +':'+ CONFIG.backendPort + CONFIG.backendAPIPath + path;
	},

	/* Tell frontend to load dummy data instead of data retrieved from backend */
	'dummyData': false
};

// Exports CONFIG in order to be returned by require() (used in grunt)
if (typeof module !== 'undefined') {
	module.exports = CONFIG;
}
