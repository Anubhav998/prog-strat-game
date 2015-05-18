app.config(["$routeProvider", function ($routeProvider) {
    "use strict";
    $routeProvider.when('/',
        {
            controller: 'HomeController',
            templateUrl: '/static/apps/game/views/home.html',
            resolve: {}
        })
        .otherwise({redirectTo: '/'});
}]);