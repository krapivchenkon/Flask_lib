

### the goals are:
- to check how application and request contexts are working in flask  
    - before first request app object can be modified safely
- check how to work with contexts from application shell


Continuing with the docs, there are two ways to create an application context:
- Automatically, whenever a request context is pushed.
- Manually, by using the app_context() method.

So how populated both stacks? On request Flask:

1. create request_context by environment (init map_adapter, match path)
enter or push this request:
  2. clear previous request_context
  3. create app_context if it missed and pushed to application context stack
  4. this request pushed to request context stack
  5. init session if it missed
6. dispatch request
7. clear request and pop it from stack

---
The app context works like the request context but can also be used for 
situations like scripts in which there is no request to handle but you 
might still want current_app and g to work. 

If you are doing something request independent use the app context  (such 
as database access) otherwise use the request context. 
--- http://librelist.com/browser//flask/2014/6/26/teardown-appcontext-and-teardown-request/#86b5596d75c10fdc7480b0f139499c34
to get access to debugger:
    import pdb; pdb.set_trace()

http://flask.pocoo.org/docs/0.10/appcontext/


> preprocess_request()
> Called before the actual request dispatching and will call every as before_request() decorated function. If any of these function returns a value it’s handled>  as if it was the return value from the view and further request handling is stoppe> d.


## Teardown callbacks
```
with app.test_client() as client:
    resp = client.get('/foo')
    # the teardown functions are still not called at that point
    # even though the response ended and you have the response
    # object in your hand

# only when the code reaches this point the teardown functions
# are called.  Alternatively the same thing happens if another
# request was triggered from the test client
```

> flask.current_app
> Points to the application handling the request. This is useful for extensions that want to support multiple applications running side by side. This is powered by the application context and not by the request context, so you can change the value of this proxy by using the app_context() method.


> Flask activates (or pushes) the application and request contexts before dispatching a
> request and then removes them when the request is handled. When the application
> context is pushed, the current_app and g variables become available to the thread;
> likewise, when the request context is pushed, request and session become available
> as well. If any of these variables are accessed without an active application or request
> context, an error is generated. 

From http://flask.pocoo.org/docs/0.10/extensiondev/#the-extension-code
# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


## testing from shell

>>> ctx = app.test_request_context()
>>> ctx= app.test_request_context('/index')

Normally you would use the with statement to make this request object active, but in the shell it’s easier to use the push() and pop() methods by hand:

>>> ctx.push()
From that point onwards you can work with the request object until you call pop:
>>> from flask import request, url_for
>>> ctx= app.test_request_context('/index/')
>>> ctx.push()
>>> app.preprocess_request()
>>> rv = app.dispatch_request()
>>> rv
'Hello World'
>>> response = app.make_response(rv)
>>> response.data
'Hello World'
>>> response = app.process_response(response)
>>> response.data
'Hello World'
>>> ctx.pop()
teardown_request called





    def full_dispatch_request(self):
        """Dispatches the request and on top of that performs request
        pre and postprocessing as well as HTTP exception catching and
        error handling.

        .. versionadded:: 0.7
        """
        self.try_trigger_before_first_request_functions()
        try:
            request_started.send(self)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
        except Exception as e:
            rv = self.handle_user_exception(e)
        response = self.make_response(rv)
        response = self.process_response(response)
        request_finished.send(self, response=response)
        return response
