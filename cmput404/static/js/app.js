'use strict';

// Declare app level module which depends on views, and components
angular.module('cmput404client', []).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
});
