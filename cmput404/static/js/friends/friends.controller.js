var app = angular.module("cmput404client")
app.controller("friendsCtrl", ['$scope', 'Author', function($scope, Author) {

    $scope.friends = [];

    Author.getCurrentFriends().then(function(friends) {
        $scope.friends = friends;
        console.log(friends);
    });

    $scope.removeFriend = function(friend_id) {
        Author.removeFriend(friend_id).then(function(res) {
            var index = -1;

            for (var i =0; i < $scope.friends.length; i++) {
                if ($scope.friends[i].id == friend_id) {
                    index = i;
                    break;
                }
            }

            if (index > -1) {
                $scope.friends.splice(index, 1);
            }
        })
    }
}]);
