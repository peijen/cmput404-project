var app = angular.module('cmput404client');
app.service('Stream', ['$q', '$http', 'djangoUrl', function($q, $http, djangoUrl) {

	this.getPosts = function() {
		var deferred = $q.defer();

		// "a GET without a postfixed “postid” should return a list of all “PUBLIC” visibility posts on your node"

		$http.get('/service/author/posts').then(function(response) {
			posts = response.data ? response.data.posts : []
			deferred.resolve(posts);
		}, function(response) {
			deferred.reject(response.status);
		});

		return deferred.promise;
	};

	this.getPost = function(post_id) {
		var deferred = $q.defer();

		$http.get('/service/author/posts/' + post_id).then(function(reponse) {
			deferred.resolve(response.data);
		}, function(response) {
			deferred.reject(response.data);
		})

		return deferred.promise;
	};

	this.commentOnPost = function(post_id, text) {
		var deferred = $q.defer();

		var comment_object = {
			comment: text,
			contentType: 'text/plain'
		}

		var url = djangoUrl.reverse('service:comment_handler', { id: post_id });
		$http.post(url, comment_object).then(function(response) {
			deferred.resolve(response.data);
		}, function(response) {
			deferred.resolve(response.status);
		});

		return deferred.promise;
	}

	this.deletePost = function(post_id) {
		var url = djangoUrl.reverse('service:post_handler_specific', { id: post_id });
		return $http.delete(url);
	}

}]);
