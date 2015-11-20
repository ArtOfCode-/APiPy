import unittest as ut
from src.requester import *


class TestAPIRequester(ut.TestCase):
    def setUp(self):
        self.requester = APIRequester("key", "id", "token")

    def test_has_request_token(self):
        self.assertTrue(self.requester.has_request_token('request_key'))
        self.assertTrue(self.requester.has_request_token('client_id'))
        self.assertTrue(self.requester.has_request_token('access_token'))

    def test_get_request_token(self):
        self.assertEqual(self.requester.get_request_token('request_key'), "key")
        self.assertEqual(self.requester.get_request_token('client_id'), "id")
        self.assertEqual(self.requester.get_request_token('access_token'), "token")

    def test_set_request_token(self):
        self.requester.set_request_token('request_key', "new_key")
        self.requester.set_request_token('client_id', "new_id")
        self.requester.set_request_token('access_token', "new_token")

        self.assertEqual(self.requester.get_request_token('request_key'), "new_key")
        self.assertEqual(self.requester.get_request_token('client_id'), "new_id")
        self.assertEqual(self.requester.get_request_token('access_token'), "new_token")
