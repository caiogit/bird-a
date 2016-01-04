'use strict';

/**
 * Created by caio on 03/01/16.
 */

angular.module('birdaApp')

	.filter('checkmark', function() {
		return function(input) {
			return input ? '\u2713' : '\u2718';
		};
	})

	.filter('capitalize', function() {
		return function(input) {
			return _.capitalize(input);
		};
	});
