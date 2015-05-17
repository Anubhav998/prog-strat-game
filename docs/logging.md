#Logging

The logs of this project are using angular's `$logProvider` service. By default
they are disabled, however, you can enable them in the browser by passing the proper credentials.

##Enabling Logging

To enable logging in the browser, pass the following query string on the end of your URL:

```
?debug=1&password=Rowing1
```

##Using Logging

Now that logging can be enabled and disabled for debugging, make sure you provide good,
logging via `$log.debug(message)`. This functionally replaces `console.log()`.
