"""
    This package is a hack to make it easier to work with the pc-ble-driver binding

    TODO: pc-ble-driver bindings for all relevant SD versions should be possible to load
    TODO: in the same python process.
    TODO: A factory mechanism should make available the requested SD version
"""

import sys
import argparse

from typing import List


class Settings(object):
    """
    This class should be in the parent package (tests), but since it is needed in this module
    we have to have it here (parent module import not allowed)
    """
    settings = None  # type: Settings

    def __init__(self, serial_ports, number_of_iterations, driver_log_level, baud_rate, retransmission_interval,
                 response_timeout, mtu, nrf_family):
        # type: (List[str], int, str, int, int, int, int) -> Settings
        self.serial_ports = serial_ports  # type: List[str]
        self.number_of_iterations = number_of_iterations  # type: int
        self.driver_log_level = driver_log_level  # type: str
        self.baud_rate = baud_rate  # type: int
        self.retransmission_interval = retransmission_interval  # type: int
        self.response_timeout = response_timeout  # type: int
        self.mtu = mtu  # type: int
        self.nrf_family = nrf_family  # type: str

    @classmethod
    def current(cls):
        # type: () -> Settings

        if cls.settings is None:
            cls.parse_args()

        return cls.settings

    @staticmethod
    def clean_args():
        # type: () -> List[str]
        args_to_remove = [
            '--port-a',
            '--port-b',
            '--baud-rate',
            '--response-timeout',
            '--retransmission-interval',
            '--mtu',
            '--iterations',
            '--log-level'
            '--nrf-family'
        ]

        retval = list(sys.argv)

        for arg_to_remove in args_to_remove:
            try:
                idx = retval.index(arg_to_remove)
                # Remove argument and argument value
                del retval[idx]
                del retval[idx]
            except ValueError, _:
                pass

        return retval

    @classmethod
    def parse_args(cls):
        # type: () -> Settings
        parser = argparse.ArgumentParser()
        parser.add_argument('--port-a', required=True, help='serial port A, usually BLE central')
        parser.add_argument('--port-b', required=True, help='serial port B, usually BLE peripheral')
        parser.add_argument('--baud-rate', help='baud rate', default=1000000)
        parser.add_argument('--response-timeout', type=int, help='transport response timeout', default=1500)
        parser.add_argument('--retransmission-interval',
                            type=int,
                            default=300,
                            help='transport retransmission interval'
                            )
        parser.add_argument('--mtu',
                            type=int,
                            default=150,
                            help='default BLE MTU, may be ignored in some tests')
        parser.add_argument('--iterations',
                            type=int,
                            default=10,
                            help='number of iterations (for tests supporting that')
        parser.add_argument('--log-level',
                            help='pc-ble-driver log level (trace|debug|info|warning|error|fatal)',
                            default='info')
        parser.add_argument('--nrf-family',
                            help='nRF family decides version of SoftDevice to use (NRF51|NRF52)',
                            default='NRF52'
                            )

        args = parser.parse_args()

        cls.settings = Settings(
            [args.port_a, args.port_b],
            args.iterations,
            args.log_level,
            args.baud_rate,
            args.retransmission_interval,
            args.response_timeout,
            args.mtu,
            args.nrf_family
        )

        return cls.settings


from pc_ble_driver_py import config

config.__conn_ic_id__ = Settings.current().nrf_family

from pc_ble_driver_py.ble_driver import BLEDriver, BLEAdvData, \
    BLEEvtID, BLEEnableParams, BLEGapTimeoutSrc, BLEUUID, BLEConfigCommon, BLEConfig, BLEConfigConnGatt
from pc_ble_driver_py.ble_adapter import BLEAdapter


__all__ = [
    "config",
    "BLEDriver",
    "BLEAdvData",
    "BLEEvtID",
    "BLEEnableParams",
    "BLEGapTimeoutSrc",
    "BLEUUID",
    "BLEConfigCommon",
    "BLEConfig",
    "BLEConfigConnGatt",
    "BLEAdapter",
    "Settings"]
