var app = angular.module("cmput404client")
app.controller("streamCtrl", ['$scope', '$http', 'Stream', 'Author', function($scope, $http, Stream, Author) {

	$scope.posts = [];

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
			console.log(comment.author);
			if (post.comments) {
				post.comments.push(comment);
			} else {
				post.comments = [comment];
			}
		}, function(response) {
			// handle error statuses
		});
	}

}]);
