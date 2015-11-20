import unittest as ut
from src.errors import *


class TestAPIBaseException(ut.TestCase):
    def test_get_message(self):
        ex = APIBaseException(404, "not_found", "no method found with this name")
        self.assertEqual(ex.get_message(), "API error #404 ('not_found'): no method found with this name.")


class TestUnauthorizedAccessException(ut.TestCase):
    def setUp(self):
        self.ex = UnauthorizedAccessException(403, "forbidden", "unauthorized access")

    def test_get_message(self):
        self.assertEqual(self.ex.get_message(), "The request was not authorized to take the requested action.")


class TestInvalidRequestTypeException(ut.TestCase):
    def setUp(self):
        self.ex = InvalidRequestTypeException("delete")

    def test_defaults(self):
        self.assertEqual(self.ex.allowed_types, ["get", "post"])

    def test_get_message(self):
        self.assertEqual(self.ex.get_message(),
                         "The provided request type 'delete' was not a member of the allowed request types.")
