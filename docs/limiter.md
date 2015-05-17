#Rate Limiter

Included in your `app/config` folder is `limiter.js`. This runtime config file gives access to a call rate limiter
funciton.

##Use

In a service, you can call `$rootScope.checkLimiter(defer, key, optional_time)`.

* `defer` - Pass in the defer object. It will call defer.reject() if the call is made too close the previous one.
* `key` - Pass in the key for the array of calls. Usually I pass in the service call name.
* `optiona_time` - overrides the default value which is 1 second.
