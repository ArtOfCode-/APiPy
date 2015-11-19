import requests
from .errors import *
from .response import APIResponse


class APIRequester:
    """
    Builds, handles and executes requests to the Stack Exchange API.
    """

    request_tokens = {
        'request_key': None,
        'client_id': None,
        'access_token': None
    }

    def __init__(self, request_key=None, client_id=None, access_token=None):
        """
        Initialises a new instance of the APIRequester class, used for making requests to the
        Stack Exchange API.
        :param request_key: (optional) The application's request key.
        :param client_id: (optional) The application's client ID, as assigned by Stack Apps app management.
        :param access_token: (optional) An access token to use for write operations.
        :return: An instance of the class.
        """
        self.request_tokens["request_key"] = request_key
        self.request_tokens["client_id"] = client_id
        self.request_tokens["access_token"] = access_token

    def has_request_token(self, token_name):
        """
        Checks if this class has a particular request token (where request tokens comprise request key, client ID
        and access token).
        :param token_name: A string, containing the name of the token. One of "request_key", "client_id" or
        "access_token".
        :return: True or False, indicating whether or not the token exists for this instance.
        """
        return (token_name in self.request_tokens                       # i.e. the passed token_name is a valid token
                and self.request_tokens[token_name] is not None)        # and the token has a value

    def get_request_token(self, token_name):
        """
        Gets the value of a request token, as specified by token_name. Yes, this method is completely unnecessary,
        but I like it as a style point. You don't have to use it.
        :param token_name: A string, containing the name of the token.
        :return: The value of the token, or None if it's not found.
        """
        if token_name in self.request_tokens:
            return self.request_tokens[token_name]
        else:
            return None

    def set_request_token(self, token_name, token_value):
        """
        Sets the value of the request token token_name to token_value. Another completely unnecessary method.
        :param token_name: A string, containing the name of the token.
        :param token_value: The value you wish to set token_name to.
        :return: None.
        """
        self.request_tokens[token_name] = token_value

    def make_request(self, route, data=None):
        """
        Makes a request to the API, using the route and data specified. Refer to the documentation for a full
        explanation of this method.
        :param route: The route to request to from the API. Should only be the latter part of the URL, after the
        /2.2 version indicator.
        :param data: Any additional data to use to build the request.
        :return: An APIResponse object (see: response.py) containing the response data.
        """

        # Let's only support the newest API version. Also, that trailing question mark makes no difference
        # to the request if there's no data, so might as well put it in here and save checks later.
        url = "https://api.stackexchange.com/2.2" + route + "?"

        # Most SE API requests are GET format, but a few are POST. Better let the next dev decide which they need.
        request_type = data["request_type"] if "request_type" in data else "get"

        # That said, I don't believe the API accepts PUT or DELETE, etc. So we'll limit it to that.
        if request_type is not "get" and request_type is not "post":
            raise InvalidRequestTypeException(request_type)

        if self.has_request_token("request_key"):
            data["key"] = self.get_request_token("request_key")

        if data is not None:        # 'cos if it is, we can just send the request already
            for key, value in data.items():
                if "{" + key + "}" in url:      # replace /route/{param}/action  -> /route/23;45;76/action o.e.
                    if isinstance(value, list):
                        string_value = ";".join(value)
                        url = url.replace("{" + url + "}", string_value)
                    else:
                        url = url.replace("{" + url + "}", value)  # not liking this repeated line, must be a better way
                    del data[key]
                else:
                    if request_type == "get":
                        url += str(key) + "=" + str(value) + "&"

        if request_type == "get":
            response = requests.get(url)
        elif request_type == "post":
            response = requests.post(url, data=data)
        else:
            raise InvalidRequestTypeException(request_type)     # though how did it get this far in the first place?

        return APIResponse(response.json())
