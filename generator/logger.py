import logging
import sys


class LogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "transaction_id") or not record.transaction_id:
            record.transaction_id = "global"
        return True


def setup_logger(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(transaction_id)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)
    handler.addFilter(LogFilter())
    root.addHandler(handler)
    return root
