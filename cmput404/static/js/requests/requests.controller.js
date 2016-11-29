var app = angular.module("cmput404client")
app.controller("requestCtrl", ['$scope', 'Author', function($scope, Author) {

    $scope.friend_requests = [];

    Author.getFriendRequests().then(function(res) {
        $scope.friend_requests = res.data;
    });

    $scope.acceptRequest = function(request) {
        Author.addFriend(request.author);
        for (var i = 0; i < $scope.friend_requests.length; i++) {
            if ($scope.friend_requests[i].id == request.id) {
                $scope.friend_requests[i].splice(i, 1);
                break;
            }
        }

    }

}]);
