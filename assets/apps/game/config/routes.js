app.config(["$routeProvider", function ($routeProvider) {
    "use strict";
    $routeProvider.when('/',
        {
            controller: 'HomeController',
            templateUrl: '/static/app/views/home.html',
            resolve: {}
        })
        .otherwise({redirectTo: '/'});
}]);