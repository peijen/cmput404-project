'use strict';

// Declare app level module which depends on views, and components
angular.module('cmput404client', ['djng.urls', 'ngSanitize']).config(function($interpolateProvider, $httpProvider) {
	// need these lines so that angular doesn't confuse its {{ var }} with djangos
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');

	// need these lines to include djangos csrf token into angulars http module
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
