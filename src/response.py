class APIResponse:
    """
    Contains data from and helper methods for managing responses to requests to the Stack API.
    """
    def __init__(self, response_json):
        """
        Initialises a new instance of the APIResponse class, using the given response JSON.
        :param response_json: The JSON returned from the API, in object form.
        :return: A new instance of the APIResponse class.
        """
        self.__json = response_json

    def is_error(self):
        """
        Detects whether the response represented by this instance is an error response.
        :return: True or False
        """
        return "error_id" in self.__json or "error_name" in self.__json or "error_message" in self.__json

    def get_items(self):
        """
        Gets the list of items from the response, excluding all other JSON scopes.
        :return: A list containing the API-returned items.
        """
        return self.__json["items"] if "items" in self.__json else None

    def get_wrapper(self):
        """
        Gets the JSON wrapper fields, excluding any JSON sub-scopes.
        :return: A dictionary containing the wrapper fields.
        """
        json_copy = self.__json
        if "items" in json_copy:
            del json_copy["items"]
        return json_copy

    # This method is basically just a wrapper around quota_remaining, but adds checks so that downstream code can be
    # more idiomatic:   response.get_quota_remaining()   instead of   response.__json['quota_remaining' if ...
    def get_quota_remaining(self):
        """
        Gets the remaining requests in the quota assigned to this IP and request key.
        :return: An integer, containing the remaining number of requests.
        """
        return self.__json["quota_remaining"] if "quota_remaining" in self.__json else None

    # This is another wrapper similar to get_quota_remaining, but around has_more.
    def has_more(self):
        """
        Indicates whether the returned object has more data in further pages.
        :return: True or False
        """
        return self.__json["has_more"] if "has_more" in self.__json else False

    def get_backoff(self):
        """
        Gets the backoff time that the API has mandated, if any.
        :return: An integer, or None if there is no backoff.
        """
        return self.__json["backoff"] if "backoff" in self.__json else None
