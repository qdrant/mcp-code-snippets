import os
import select
import signal
import sys
import time
import threading


def _stdin_hup():
    poller = select.poll()
    poller.register(sys.stdin, select.POLLHUP)
    while True:
        if poller.poll(1000):  # ≥1 second; does not block the thread
            os.kill(os.getpid(), signal.SIGTERM)


def _parent_watcher() -> None:
    _PARENT_PID = os.getppid()
    while True:
        if os.getppid() != _PARENT_PID:  # Parent process died
            os.kill(os.getpid(), signal.SIGTERM)  # Gracefully stop the service
        time.sleep(2)


def _graceful_exit(*_):
    print("STDIN closed or signal received, shutting down MCP server...", file=sys.stderr)
    sys.exit(0)

def watch_parent():
    # showing no love for Windows at the moment
    if os.name == "posix":
        for fn in (_parent_watcher, _stdin_hup):
            threading.Thread(target=fn, daemon=True).start()

        signal.signal(signal.SIGINT, _graceful_exit)
        signal.signal(signal.SIGTERM, _graceful_exit)
