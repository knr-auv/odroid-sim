from .pad.PadTh import PadSteeringThread
from .readpad.ReadTh import ReadSteeringThread
from .ui.UiTh import UIThread
from .test.test import TestThread
from .key.KeyTh import KeySteeringThread
from .autonomy.autonomy import Autonomy


controls = {
    "pad": PadSteeringThread,
    "read": ReadSteeringThread,
    "ui": UIThread,
    "test": TestThread,
    "key": KeySteeringThread,
    "autonomy": Autonomy
}


def get_control(pid_thread, config):
    return controls[config.get("control")](pid_thread, config)


