var app = angular.module("cmput404client")
app.controller("requestCtrl", ['$scope', 'Author', function($scope, Author) {

    $scope.friend_requests = [];

    Author.getFriendRequests().then(function(res) {
        $scope.friend_requests = res.data;
    }, function(res) {

    });

}]);
