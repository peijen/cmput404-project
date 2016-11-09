angular.module('cmput404client').filter('closeDateFilter', function($filter)
{
    return function(input) {
        var today = new Date();
        var yesterday = new Date();
        var oneWeekAgo = new Date();
        var dateInput = new Date(input);

        today.setHours(0,0,0,0);
        yesterday.setDate(today.getDate() - 1);
        yesterday.setHours(0,0,0,0);
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

        if (dateInput >= today) {
            return "Today " + $filter('date')(dateInput, 'h:mm a')
        }

        else if (dateInput < today && dateInput >= yesterday) {
            return "Yesterday " + $filter('date')(dateInput, 'h:mm a')
        }

        else if (dateInput > oneWeekAgo && dateInput < yesterday) {
            return 'on ' + $filter('date')(dateInput, 'EEE h:mm a')
        }

        else {
            return 'on ' + $filter('date')(dateInput, 'MMM d, y');
        }
    };
});
