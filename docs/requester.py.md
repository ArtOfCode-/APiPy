## Documentation for `APiPy.requester`

The `requester` sub-module contains one class, designed to build, handle and execute requests to the Stack Exchange API.
It is intended as the primary interface into APiPy, and to be used with the `response` sub-module to handle the 
returned responses.

### Class List
- [`APIRequester`](#class-apirequester)

### Class: `APIRequester`
The `APIRequester` class, as summarised, is the primary interface your code has to the library. It's intended to be a 
complete package that enables you to fire off a basic request to the API without having to touch any other classes.

#### Class Attributes
- ##### `request_tokens`  
  **Type:** Dictionary  
  Holds request tokens for this requester instance. Request tokens are defined as one of a request key, a client ID, and
  an access token. You can use this object directly for getting, setting, or checking request tokens; there are also 
  methods provided to perform those tasks if you prefer using methods.

#### Class Methods
- ##### `__init__(request_key=None, client_id=None, access_token=None)`  
  **Param `request_key`:** An *optional* request key for the API, to grant a higher request quota. Type: string.  
  **Param `client_id`:** An *optional* client ID, as provided by Stack Apps registration, identifying your application.
  Type: string.  
  **Param `access_token`:** An *optional* access token, used to give authorisation for write operations with the API. 
  Type: string.
  
  This is simply the class initializer method, and doesn't do anything special. If you pass any parameters to it, it 
  will add them to the [`request_tokens`](#request_tokens) dictionary so that they can be accessed both internally and 
  by your code at a later point. You *can* add, change or delete request tokens after initialization, though - it's not 
  imperative that you pass them in here.

- ##### `has_request_token(token_name)`  
  **Param `token_name`:** The name of the request token you want to check existence of.
  
  This is one of the methods provided to work with the [`request_tokens`](#request_tokens) dictionary, instead of 
  directly interacting with the dictionary itself. This method checks for *existence* of a particular token: that is, 
  that there is a field in the dictionary with the token's name, and that its value isn't `None`. You should pass in one 
  of `request_key`, `client_id`, or `access_token` - those are the names under which the respective tokens are stored.
  
- ##### `get_request_token(token_name)`  
  **Param `token_name`:** The name of the request token to fetch a value for.
  
  This method complements `has_request_token` and `set_request_token`. It does pretty much what it says on the tin (and 
  the docstring) - returns the value of a given request token. Returns `None` if the request token doesn't exist, or 
  `None` if that's the token's actual value. For most purposes, non-existent is functionally no different from a `None` 
  value.
  
- ##### `set_request_token(token_name, token_value)`  
  **Param `token_name`:** The name of the request token whose value you want to set.  
  **Param `token_value`:**: The new value of the token.
  
  The third of the trilogy. Again, does what it says on the signature - sets the value of the request token called 
  `token_name` to your new value in `token_value`.
  
  This method doesn't actually check whether you're using a valid request token name (i.e. `request_key`, `client_id` or 
  `access_token`), so if you have a typo it's pretty likely to cause a bug. However, this is almost a non-issue, so I 
  don't envision fixing this.
  
- ##### `make_request(route, data=None)`  
  **Param `route`:** The API route to request from.  
  **Param `data`:** Optional data to send with the request.
  
  This is the main method in the class. It takes an API route and optionally extra data to add to the request, and makes 
  the request. It returns an `APIResponse` object, which is documented in the documentation for the `response` 
  sub-module.
  
  A note on API routes. A normal URL to the SE API will look something like this:
  
      https://api.stackexchange.com/2.2/questions
      
  The *route*, as I've defined it, is the part *after* the version indicator - so in this case, it's `/questions`.
  
  In your route, you can include named parameters. Some API methods require a set of IDs (or similar) in the middle of 
  the path - you can deal with this by using a named parameter. If you pass a `route` like this:
  
      /answers/{ids}/action
      
  and *additionally* include an `ids` field in the `data` dictionary, then the `{ids}` in the route will be rewritten 
  to the data in the dictionary before sending. So, take this code:
  
      requester = APIRequester(some_request_key)
      
      request_data = {
          'ids': [27743, 29924, 34623]
      }
      
      requester.make_request("/answers/{ids}/action", data=request_data)
      
  This would, after processing, send a request to `https://api.stackexchange.com/2.2/answers/27743;29924;34623/action`. 
  The name of the parameter doesn't have to be 'ids', and it can be either a string to substitute, or a list (which will 
  be joined with semicolons).