var app = angular.module("cmput404client")
app.controller("authorCtrl", ['$scope', 'Author', function($scope, Author) {



    $scope.addFriend = function() {
        var re = new RegExp(String.fromCharCode(160), "g"); //remove any &nbsp
        var author = {
            'id': $('#author_id').text().replace(re, ""),
            'displayName': $('#display_name').text().replace(re, ""),
            'host': $('#author_host').text().replace(re, ""),
            'url': $('#author_url').text().replace(re, "")
        }
        Author.addFriend(author);
    }

}]);
