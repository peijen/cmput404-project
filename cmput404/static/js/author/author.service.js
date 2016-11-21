var app = angular.module('cmput404client');
app.service('Author', ['$q', '$http', 'djangoUrl', function($q, $http, djangoUrl) {



    var _this = this; // Save the context
    _this.user = {};

    this.getUserAndAuthorProfile = function() {
        var deferred = $q.defer();

        var url = djangoUrl.reverse('service:me');
        $http.get(url).then(function(response) {
            deferred.resolve(response.data);
        }, function(response) {
            deferred.resolve(response.status);
        });

        return deferred.promise;
    }

	this.getMe = function() {
		var deferred = $q.defer();

        _this.getUserAndAuthorProfile().then(function(user) {
            _this.user = user;
            deferred.resolve(user);
        }, deferred.reject)

		return deferred.promise;
	};

    this.getCurrentUser = function() {
        return _this.user;
    }

    var init = function() {
        _this.getMe();
    }

    init();

}]);
