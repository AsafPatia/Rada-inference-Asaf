import argparse
import sys
from config.settings import settings
import logging
import ipaddress

# TODO: fix the version
# TODO: make sure Types are OK
# TODO: Understand how to run -h


logger = logging.getLogger(__name__)


def handle_cli(argv):
    args = parse_args(argv)

    try:
        ipaddress.ip_address(args.HostIP)
    except (ValueError, TypeError):
        print('Invalid IP')
        logger.debug("Exiting - Illegal HostIP used in CLI: %s", argv)
        sys.exit(2)

    try:
        ipaddress.ip_address(args.ClientIP)
    except (ValueError, TypeError):
        print('Invalid IP')
        logger.debug("Exiting - Illegal HostIP used in CLI: %s", argv)
        sys.exit(2)

    try:
        val = int(args.HostPort)
        # if val < 0:
        #     raise ValueError
    except ValueError:
        print('Invalid Port')
        sys.exit(2)

    settings.host_ip = args.HostIP
    settings.host_port = int(args.HostPort)
    settings.client_ip = args.ClientIP
    settings.client_port = int(args.ClientPort)
    settings.unknown_prediction_code = int(args.UnknownPredictionCode)
    settings.drone_prediction_code = int(args.DronePredictionCode)
    settings.not_drone_prediction_code = int(args.NotDronePredictionCode)
    settings.plot_sliding_window_size = int(args.PlotSlidingWindowSize)
    settings.idle_track_purging_frequency = int(args.IdleTrackPurgingFrequency)


def parse_args(args):
    # TODO change ClientPort to 7034
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--ver', type=str, help='BMRadarTargetClassification Version 0.1')
    parser.add_argument('--HostIP', type=str, default='127.0.0.1', help='Inbound messages IP Address')
    parser.add_argument('--HostPort', type=str, default='7033', help='Inbound messages listener Port')
    parser.add_argument('--ClientIP', type=str, default='127.0.0.1', help='Outbound messages client IP')
    parser.add_argument('--ClientPort', type=str, default='7033', help='Outbound messages client Port')
    parser.add_argument('--UnknownPredictionCode', type=str, default='1', help='To be used as QuamCu TargetType value')
    parser.add_argument('--DronePredictionCode', type=str, default='8', help='To be used as QuamCu TargetType value')
    parser.add_argument('--NotDronePredictionCode', type=str, default='9',
                        help='To be used as QuamCu TargetType value')
    parser.add_argument('--PlotSlidingWindowSize', type=str, default='10', help='The size of sliding window in memory')
    parser.add_argument('--IdleTrackPurgingFrequency', type=str, default='10', help='The amount of seconds an' + \
                                                                                    'idle trackID will be kept before '
                                                                                    'it is purged.')
    return parser.parse_args(args)
