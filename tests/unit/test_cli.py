import unittest
import pytest
from config.settings import settings
from utils.CLI import handle_cli
from utils.CLI import parse_args
import contextlib
import io


# TODO: How to check that the IP and PORT do exist
# TODO: Fixing illegal Input - raise an error and need to catch it

class TestCLI(unittest.TestCase):
    # ================================= Placement Tests ====================================================
    def test_cli_host_ip_placement(self):
        argv = ['--HostIP', '129.0.0.1', '--HostPort', '9008']
        handle_cli(argv)
        self.assertEqual("129.0.0.1", settings.host_ip)
        self.assertEqual(9008, settings.host_port)

    def test_cli_client_ip_placement(self):
        argv = ['--ClientIP', '127.0.0.1', '--ClientPort', '8080']
        handle_cli(argv)
        self.assertEqual("127.0.0.1", settings.client_ip)
        self.assertEqual(8080, settings.client_port)

    def test_cli_unknown_prediction_code_placement(self):
        argv = ['--UnknownPredictionCode', '0']
        handle_cli(argv)
        self.assertEqual(0, settings.unknown_prediction_code)

    def test_cli_drone_prediction_code_placement(self):
        argv = ['--DronePredictionCode', '0']
        handle_cli(argv)
        self.assertEqual(0, settings.drone_prediction_code)

    def test_cli_drone_not_prediction_code_placement(self):
        argv = ['--NotDronePredictionCode', '7']
        handle_cli(argv)
        self.assertEqual(7, settings.not_drone_prediction_code)

    def test_cli_plot_sliding_window_size_placement(self):
        argv = ['--PlotSlidingWindowSize', '50']
        handle_cli(argv)
        self.assertEqual(50, settings.plot_sliding_window_size)

    def test_cli_idle_track_purging_frequency_placement(self):
        argv = ['--IdleTrackPurgingFrequency', '5']
        handle_cli(argv)
        self.assertEqual(5, settings.idle_track_purging_frequency)

    # ================================ illegal Name Of Input ===========================================
    def test_cli_illegal_host_ip_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--HostiP', '127.0.0.1']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_host_port_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--Host Port', '8080']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_clint_ip_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--clientIP', '127.0.0.1']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_clint_port_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--clientPort', '8080']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_UnknownPredictionCode_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--UnknownPredictionCODE', '5']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_DronePredictionCode_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--DRONEPredictionCode', '5']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_NotDronePredictionCode_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--NotDRONEPredictionCode', '5']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_PlotSlidingWindowSize_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--PlotSlidingwindowSize', '50']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_IdleTrackPurgingFrequency_args(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            # sending illegal args that should cause the app to exit with error code 2
            argv = ['--IdleTrackPurgingFrequencY', '5']
            handle_cli(argv)

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    # =============================== illegal Input =======================================================
    def test_cli_illegal_host_ip(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['--HostIP', '127.0.1']
            handle_cli(argv)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_host_ip_1(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['--HostIP', '300.0.1.0']
            handle_cli(argv)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_host_ip_2(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['--HostIP', '300.0.1.a']
            handle_cli(argv)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_client_ip(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['--ClientIP', '127.0.1']
            handle_cli(argv)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_client_ip_1(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['--ClientIP', '300.0.1.0']
            handle_cli(argv)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    def test_cli_illegal_client_ip_2(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            argv = ['--ClientIP', '300.0.1.a']
            handle_cli(argv)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2


if __name__ == '__main__':
    unittest.main()