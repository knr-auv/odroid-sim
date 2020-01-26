import threading


class TestThread(threading.Thread):
    """Only for testing """

    def __init__(self, pid_thread, config):
        threading.Thread.__init__(self)

    def run(self):
        pass
