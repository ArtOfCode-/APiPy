## Documentation for `APiPy.response`

The `response` sub-module complements the requester sub-module: the requester returns a response object, which is an
instance of the class in this module: the `APIResponse` class.

### Class List
- [`APIResponse`](#class-apiresponse)

### Class: `APIResponse`
The `APIResponse` class is designed for dealing with API responses. It will be passed the response from the requester,
and makes available helper methods for dealing with the response and getting hold of the data.

#### Class Methods
- ##### `__init__(response_json)`  
  **Param `response_json`:** A JSON object containing the response returned by the API.
  
  This is the class initializer method. You will likely never need to worry about this in normal use, unless you intend
  to make your own version of this class by extending it. It takes in a JSON dictionary, as returned by the API, and 
  stores it in a private variable so that the various other class methods can access it.
  
- ##### `is_error()`  
  Pretty much as it says on the tin. This is a helper method, and will detect if the response stored in this instance 
  contains error details and thus represents an error response. To do this, it looks for any of the `error_*` fields, 
  i.e. `error_id`, `error_name`, or `error_message`.
  
- ##### `get_items()`  
  Most of these methods are pretty self-explanatory. This one will find and return the list of items contained in the
  response, and will exclude all the wrapper fields. Be aware that there is not always such a list, especially if the
  response is an error. Hence, this method is more useful when combined with `is_error()`:
  
      if not response.is_error():
          item_list = response.get_items()
  
- ##### `get_wrapper()`  
  This is the complement to `get_items()`: it finds and returns as a dictionary all the fields in the API wrapper 
  object. These are meta-fields about the request *itself*, like the `error_*` fields, or `quota_remaining`. This 
  essentially means that the `items` 'sub-scope' is removed. If you have some response JSON like this:
  
      {
          'quota_remaining': 9974,
          'has_more': true,
          'backoff': 10,
          'items': [
              {
                  'question_id': 1138236,
                  'score': 666
              }
          ]
      }
      
  then you'll end up with the `items` object removed, and this JSON returned as a dictionary:
  
      {
          'quota_remaining': 9974,
          'has_more': true,
          'backoff': 10
      }
  
- ##### `get_quota_remaining()`  
  The effect of this helper method can be achieved without a whole lot more effort, using the `get_wrapper()` dictionary
  and checking for the `quota_remaining` field. However, this makes code a lot more idiomatic and pretty. It'll return 
  the number of requests you've got left in your quota, or `None` if it can't find the field (though I've never 
  encountered that situation with real API responses).
  
- ##### `has_more()`  
  Again, this pretty much just wraps the wrapper's `has_more` field. However, it removes the checking you have to do on 
  the wrapper dictionary. Will return `True` if the `has_more` field is set to `true`, or `False` if the field is 
  `false` or can't be found in the dictionary.
  
- ##### `get_backoff()`  
  Will find and return the `backoff` field from the wrapper. This is similar to the last two methods in that it's a 
  wrapper method around a field intended to make code semantically nicer.
  
  As per the [API documentation on rate limiting](https://api.stackexchange.com/docs/throttle), this field is measured 
  in *seconds*. A return of 5 means 'wait 5 seconds before hitting the same route again'. Additionally, *any* API route 
  can return a `backoff` field, so I strongly recommend you check this method for every request you intend to repeat.