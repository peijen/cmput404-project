var app = angular.module('cmput404client');
app.service('Author', ['$q', '$http', '$location', 'djangoUrl', function($q, $http, $location, djangoUrl) {

    var _this = this; // Save the context
    var deferred_friends = $q.defer();
    _this.user = {};
    _this.friends = deferred_friends.promise;

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

    this.addFriend = function(friend) {
        var host = "https://cmput404t02.herokuapp.com/service/";
        var currentUser = _this.getCurrentUser();

        var data = {
            'query': 'friendrequest',
            'author': currentUser.author,
            'friend': friend
        }

        if (friend.host !== host) {
            _this.addFriendRemote(friend, data).then(_this.addFriendLocal(data));
        }

        else {
            _this.addFriendLocal(data);
        }
    }

    this.addFriendRemote = function(friend, data) {
        return $http.post(friend.host + 'friendrequest', data);
    }

    this.addFriendLocal = function(data) {
        var url = djangoUrl.reverse('service:friendrequest_handler');
        return $http.post(url, data);
    }

    this.getFriendRequests = function() {
        var url = djangoUrl.reverse('service:friendrequest_handler')
        return $http.get(url);
    }

    this.getFriends = function() {
        var deferred = $q.defer();
        var url = djangoUrl.reverse('service:friend_handler')
        $http.get(url).then(function(res) {
            deferred_friends.resolve(res.data);
            deferred.resolve(res.data);
        }, deferred.reject)
        return deferred.promise;
    }

    this.getCurrentFriends = function() {
        return _this.friends;
    }

    this.removeFriend = function(friend_id) {
        var url = djangoUrl.reverse('service:friend_handler_specific', {id: friend_id})
        return $http.delete(url);
    }

    var init = function() {
        _this.getMe();
        _this.getFriends();
    }

    init();

}]);
