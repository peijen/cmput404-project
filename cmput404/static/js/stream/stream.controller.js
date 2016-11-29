var app = angular.module("cmput404client")
app.controller("streamCtrl", ['$scope', '$http', 'Stream', 'Author', function($scope, $http, Stream, Author) {

	$scope.posts = [];
	$scope.getCurrentUser = Author.getCurrentUser;

	Stream.getPosts().then(function(posts) {
		$scope.posts = posts;
		return;
	}, function(status) {
		// handle error statuses
	});

	$scope.addComment = function(post, comment_text) {
		post.comment = "";

		Stream.commentOnPost(post.id, comment_text).then(function(comment) {
			comment.author = Author.getCurrentUser().author;
			if (post.comments) {
				post.comments.push(comment);
			} else {
				post.comments = [comment];
			}
		}, function(response) {
			// handle error statuses
		});
	}

	$scope.deletePost = function(post_id) {
		Stream.deletePost(post_id).then(function(res) {
			var index = -1;
			for(var i = 0; i < $scope.posts.length; i++) {
				if ($scope.posts[i].id == post_id) {
					index = i;
					break;
				}
			}
			if (index > -1) {
    			$scope.posts.splice(index, 1);
			}
		}, function(res) {

		})
	}

}]);
