import csv
import os
from _csv import register_dialect
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR


class excel_backslash(csv.excel):
    """Standard excel dialect that support backslash character."""
    escapechar = "\\"


register_dialect("excel-backslash", excel_backslash)


def unlock_file(filename):
    if os.path.exists(filename):
        os.chmod(filename, S_IWUSR | S_IREAD)


def lock_file(filename):
    os.chmod(filename, S_IREAD | S_IRGRP | S_IROTH)
