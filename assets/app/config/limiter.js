app.run(["$rootScope", "$log", function ($rootScope, $log) {
    "use strict";
    $rootScope.limiter = {};
    $rootScope.limit = 1000; // 1 second

    $rootScope.checkLimiter = function (d, key, limit) {
        var timeSinceLastGet = $rootScope.limiter[key] ? new Date().getTime() - $rootScope.limiter[key] : null,
            rlimit = limit || $rootScope.limit;
        if ($rootScope.limiter[key] && timeSinceLastGet < rlimit) {
            $log.debug('call rejected', $rootScope.limiter);
            d.reject();
        }
        $rootScope.limiter[key] = new Date().getTime();
    };
}]);