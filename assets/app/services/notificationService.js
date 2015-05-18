app.service('NotificationService', ["$http", "$q", "$rootScope", function ($http, $q, $rootScope) {
    'use strict';
    return {
        listNotifications: function () {
            var defer = $q.defer();
            $rootScope.checkLimiter(defer, 'list-notifications', 3000);
            $http({
                method: "GET",
                url: "/api/notifications/"
            }).success(function (data, status, headers, config) {
                defer.resolve(data);
            }).error(function (data, status, headers, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        deleteNotifications: function (id) {
            var defer = $q.defer();
            $rootScope.checkLimiter(defer, 'delete-notification-' + id);
            $http({
                method: "DELETE",
                url: "/api/notifications/" + id + "/"
            }).success(function (data, status, headers, config) {
                defer.resolve(data);
            }).error(function (data, status, headers, config) {
                defer.reject(status);
            });
            return defer.promise;
        }

    };
}]);