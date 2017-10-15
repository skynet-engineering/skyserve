from unittest import TestCase

from src.handlers.base_handler import BaseHandler


class TestBaseHandler(TestCase):
    def setUp(self):
        self.instance = BaseHandler()

    def test_class_properties(self):
        self.assertEqual(self.instance.path, '')
        self.assertFalse(self.instance.async)
        self.assertIsNotNone(self.instance.logger)

    def test_run(self):
        self.assertRaises(
            NotImplementedError,
            self.instance.run,
        )
