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

    def get_quota_remaining(self):
        """
        Gets the remaining requests in the quota assigned to this IP and request key.
        :return: An integer, containing the remaining number of requests.
        """
        return self.__json["quota_remaining"] if "quota_remaining" in self.__json else None
