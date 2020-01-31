from .pad.PadTh import PadSteeringThread
from .readpad.ReadTh import ReadSteeringThread
from .ui.UiTh import UIThread
from .test.test import TestThread
from .key.KeyTh import KeySteeringThread


controls = {
    "pad": PadSteeringThread,
    "read": ReadSteeringThread,
    "ui": UIThread,
    "test": TestThread,
    "key": KeySteeringThread
}


def get_control(pid_thread, config):
    return controls[config.get("control")](pid_thread, config)


