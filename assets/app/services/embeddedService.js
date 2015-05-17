app.service('EmbeddedService', [
    "$http",
    "$q",
    "CacheFactory",
    function ($http, $q, CacheFactory) {
        'use strict';

        return {
            getObjectFromUrl: function (url, cache, bust) {
                cache = cache ? CacheFactory.get('defaultCache') : false;
                if (cache && bust) {
                    cache.remove(url);
                }
                var defer = $q.defer();
                $http({
                    method: "GET",
                    cache: cache,
                    url: url
                }).success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
                return defer.promise;
            },
            postObjectToUrl: function (url, data) {
                var defer = $q.defer();
                $http({
                    method: "POST",
                    data: data,
                    url: url
                }).success(function (data, status, headers, config) {
                    var cache = CacheFactory.get("defaultCache");
                    cache.put(url, data);
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
                return defer.promise;
            },
            bustCache: function (url) {
                var cache = CacheFactory.get('defaultCache');
                cache.remove(url);
            }
        };
    }]);