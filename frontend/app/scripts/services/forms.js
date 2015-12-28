/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('formsService', function() {
		this.query = null;
		this.forms = null;

		this.retriveForms = function() {
			return "Hello, World!"
		};
	});
