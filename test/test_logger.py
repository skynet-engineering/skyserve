import time
from unittest import TestCase

import mock

from logger import LogLevel
from logger import Logger


class TestLogger(TestCase):
    def setUp(self):
        self.logger = Logger('name')

    def test_log_levels(self):
        self.assertIsNotNone(LogLevel.DEBUG)
        self.assertIsNotNone(LogLevel.INFO)
        self.assertIsNotNone(LogLevel.WARN)
        self.assertIsNotNone(LogLevel.ERROR)

    @mock.patch.object(time, 'strftime', return_value='01:01:01')
    @mock.patch.object(Logger, '_print_stdout')
    def test_log_debug(self, mock_print, mock_time):
        self.logger.debug('message')
        mock_print.assert_called_once_with('[01:01:01] [name] [DEBUG] message')

    @mock.patch.object(time, 'strftime', return_value='01:01:01')
    @mock.patch.object(Logger, '_print_stdout')
    def test_log_info(self, mock_print, mock_time):
        self.logger.info('message')
        mock_print.assert_called_once_with('[01:01:01] [name] [INFO] message')

    @mock.patch.object(time, 'strftime', return_value='01:01:01')
    @mock.patch.object(Logger, '_print_stdout')
    def test_log_warn(self, mock_print, mock_time):
        self.logger.warn('message')
        mock_print.assert_called_once_with('[01:01:01] [name] [WARN] message')

    @mock.patch.object(time, 'strftime', return_value='01:01:01')
    @mock.patch.object(Logger, '_print_stdout')
    def test_log_error(self, mock_print, mock_time):
        self.logger.error('message')
        mock_print.assert_called_once_with('[01:01:01] [name] [ERROR] message')
