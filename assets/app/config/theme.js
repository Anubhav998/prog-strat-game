app.config(['$mdThemingProvider', function ($mdThemingProvider) {
    "use strict";
    $mdThemingProvider.theme('default')
        .primaryPalette('blue')
        .accentPalette('light-blue')
        .warnPalette('red')
        .backgroundPalette('grey')
        .dark();
}]);