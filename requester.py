from errors import *


class APIRequester:
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
        self.request_key = request_key
        self.client_id = client_id
        self.access_token = access_token

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

    def make_request(self, route, data=None):
        """
        Makes a request to the API, using the route and data specified. Refer to the documentation for a full
        explanation of this method.
        :param route: The route to request to from the API. Should only be the latter part of the URL, after the
        /2.2 version indicator.
        :param data:
        :return:
        """
        url = "https://api.stackexchange.com/2.2" + route
        if data is not None:
            for key, value in data.items():
                if "{" + key + "}" in url:
                    if isinstance(value, list):
                        string_value = ";".join(value)
                        url = url.replace("{" + url + "}", string_value)
                    else:
                        url = url.replace("{" + url + "}", value)
