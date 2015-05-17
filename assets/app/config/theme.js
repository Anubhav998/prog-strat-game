app.config(['$mdThemingProvider', function ($mdThemingProvider) {
    "use strict";
    $mdThemingProvider.theme('default')
        .primaryPalette('teal')
        .accentPalette('cyan')
        .warnPalette('red')
        .backgroundPalette('grey');
}]);