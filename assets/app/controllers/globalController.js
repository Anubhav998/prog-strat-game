app.controller("GlobalController", [
    "$scope",
    "$rootScope",
    "$location",
    "$log",
    function ($scope, $rootScope, $location, $log) {
        'use strict';
        $log.debug("Global Controller Initialized");

         // global help functions
        $scope.go = function () {
            var args = Array.prototype.slice.call(arguments),
                url = "/" + args.join('/');
            url = url.replace('//', '/');
            $log.debug('go', url);
            $location.path(url);
        };

        $scope.goRel = function () {
            var args = Array.prototype.slice.call(arguments),
                url = "/" + args.join('/');
            url = url.replace('//', '/');
            $log.debug('go', url);
            $location.path($location.path() + url);
        };

        $scope.onPage = function () {
            var args = Array.prototype.slice.call(arguments),
                url = "/" + args.join('/') + '/';
            url = url.replace('//', '/');
            return $location.path().indexOf(url) !== -1;
        };

        $scope.open = function (url) {
            window.open(url, '_blank');
        };

        $scope.reload = function () {
            $route.reload();
        };

        $scope.onLarge = function (classname) {
            if ($mdMedia('gt-md')) {
                return classname;
            }
        };

        $scope.signout = function () {
            window.location.href = 'logout';
        };

        //heartbeat
        setInterval(function () {
            $rootScope.$broadcast('heartbeat');
        }, 60000);
    }]);