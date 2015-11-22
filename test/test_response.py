import unittest as ut
from src.response import *


# This response is fictional. It could never be returned from the API, but for the sake of a
# complete test, I'm using it.
test_json = {
    # backoff should be detected by get_backoff
    'backoff': 5000,

    # should make is_error return true
    'error_id': 404,

    # should turn up in get_quota_remaining
    'quota_remaining': 9476,

    # this is a list of question objects
    'items': [
        {
            'tags': [
                'windows', 'c#', '.net'
            ],
            'question_id': 1128942,
            'score': 12
        },
        {
            'tags': [
                'apple-script', 'java', 'google'
            ],
            'question_id': 1128487,
            'score': -7
        }
    ]
}

class TestAPIResponse(ut.TestCase):
    def setUp(self):
        self.response = APIResponse(test_json)

    def test_is_error(self):
        self.assertTrue(self.response.is_error())

    def test_get_items(self):
        self.assertTrue(isinstance(self.response.get_items(), list))
        self.assertEqual(len(self.response.get_items()), 2)

    def test_get_wrapper(self):
        self.assertTrue(isinstance(self.response.get_wrapper(), dict))
        self.assertTrue("items" not in self.response.get_wrapper())

    def test_get_quota_remaining(self):
        self.assertEqual(self.response.get_quota_remaining(), 9476)

    def test_has_more(self):
        self.assertTrue(not self.response.has_more())

    def test_get_backoff(self):
        self.assertEqual(self.response.get_backoff(), 5000)
