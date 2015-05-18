app.controller("NotificationController", [
    "$scope",
    "$log",
    "$q",
    "$rootScope",
    "NotificationService",
    "EmbeddedService",
    function ($scope, $log, $q, $rootScope, NotificationService, EmbeddedService) {
        'use strict';
        $log.debug("Notification Controller Initialized");

        $scope.apiVersion = false;

        $scope.checkNotifications = function () {
            NotificationService.listNotifications().then(function (data) {
                var notifications = [], promise, promises = [];
                angular.forEach(data, function (notification) {
                    promise = EmbeddedService.getObjectFromUrl(notification.actor, true).then(function (user) {
                        notification.user = user;
                        notifications.push(notification);
                    });
                    promises.push(promise);
                });
                $q.all(promises).then(function () {
                    $rootScope.$broadcast('notifications-loaded', notifications);
                });
            });
        };

        $scope.checkNotifications();

        $rootScope.$on('heartbeat', function () {
            $scope.checkNotifications();
        });

    }]);