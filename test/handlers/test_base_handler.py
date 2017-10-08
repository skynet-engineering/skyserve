from unittest import TestCase

from handlers.base_handler import BaseHandler


class TestBaseHandler(TestCase):
    def setUp(self):
        self.instance = BaseHandler()

    def test_class_properties(self):
        self.assertEqual(self.instance.path, '')
        self.assertFalse(self.instance.async)

    def test_run(self):
        self.assertRaises(
            NotImplementedError,
            self.instance.run,
        )
