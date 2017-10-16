import mock
from mock import patch
from unittest import TestCase

from src.handlers.mixins.avionics_mixin import AvionicsMixin


class TestAvionicsMixin(TestCase):

    @patch("src.handlers.mixins.avionics_mixin.AvionicsMixin.connect_vehicle")
    def test_automatic_connection(self, connect_vehicle):
        """
        If the vehicle is not connected, a call to vehicle() will connect it.
        Subsequent calls do not establish a new connection if already connected.
        """
        self.reset_avionics()
        AvionicsMixin.vehicle()
        connect_vehicle.assert_called_once()
        AvionicsMixin._vehicle = True
        AvionicsMixin.vehicle()
        connect_vehicle.assert_called_once()

    @patch("src.handlers.mixins.avionics_mixin.logger")
    @patch("src.handlers.mixins.avionics_mixin.dronekit_sitl")
    @patch("src.handlers.mixins.avionics_mixin.connect")
    def test_uses_sitl_backup(self, mock_connect, mock_sitl, mock_logger):
        """
        The AvionicsMixin uses SITL iff no connection string was offered.
        """
        # Connect the vehicle with no connection string. SITL should be used.
        self.reset_avionics()
        AvionicsMixin.connect_vehicle()
        mock_sitl.start_default.assert_called_once()
        # Connect the vehicle with a connection string. SITL shouldn't be used.
        self.reset_avionics()
        mock_sitl.start_default.reset_mock()
        AvionicsMixin.connection_string = "tcp:127.0.0.1:9999"
        AvionicsMixin.connect_vehicle()
        mock_sitl.start_default.assert_not_called()

    @patch("src.handlers.mixins.avionics_mixin.time")
    def test_only_arms_when_needed(self, mock_time):
        """
        The vehicle is only armed if not already.
        """
        mock_time.time = mock.MagicMock()
        self.reset_avionics()
        AvionicsMixin._vehicle = mock.MagicMock()
        AvionicsMixin._vehicle.armed = True
        self.assertTrue(AvionicsMixin.ensure_armed(timeout=0))
        # Make sure we gave up before ever attempting to check if the vehicle
        # was armable.
        mock_time.time.assert_not_called()

    @patch("src.handlers.mixins.avionics_mixin.time")
    @patch("src.handlers.mixins.avionics_mixin.logger")
    def test_arm_can_timeout(self, mock_logger, mock_time):
        """
        Arming the vehicle can time out.
        """
        # Time is "0" when asked the first time; "100" when asked the second.
        mock_time.time.side_effect = [0.0, 100.0]
        self.reset_avionics()
        AvionicsMixin._vehicle = mock.MagicMock()
        AvionicsMixin._vehicle.is_armable = False
        AvionicsMixin._vehicle.armed = False
        self.assertFalse(AvionicsMixin.ensure_armed(timeout=99.9))
        self.assertEquals(mock_time.time.call_count, 2)

    def test_cleanup(self):
        """
        'Cleanup' cleanly closes the connection to the vehicle and stops SITL.
        """
        self.reset_avionics()
        AvionicsMixin._vehicle = mock.MagicMock()
        AvionicsMixin.sitl = mock.MagicMock()
        AvionicsMixin.cleanup()
        AvionicsMixin.sitl.stop.assert_called_once()
        AvionicsMixin._vehicle.close.assert_called_once()

    @staticmethod
    def reset_avionics():
        """
        Reset the AvionicsMixin to its starting state.
        """
        AvionicsMixin._vehicle = None
        AvionicsMixin.connection_string = None
        AvionicsMixin.sitl = None
