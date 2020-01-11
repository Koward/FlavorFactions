import csv
import os
from _csv import register_dialect
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

import pandas as pd


class excel_backslash(csv.excel):
    """Standard excel dialect that support backslash character."""
    escapechar = "\\"


register_dialect("excel-backslash", excel_backslash)


def unlock_file(filename):
    """Ensures the file can be written to."""
    if os.path.exists(filename):
        os.chmod(filename, S_IWUSR | S_IREAD)


def lock_file(filename):
    """Prevents file from being accidentally edited."""
    os.chmod(filename, S_IREAD | S_IRGRP | S_IROTH)


def merge_update_csv_files(csv_files, primary_key):
    """
    From multiple csv files, apply them on top of each other.
    Based on primary key, matching entries are overriden while new ones are added.
    :param csv_files: A list of CSV files paths.
    :param primary_key: Primary key string used to match entries between themselves.
    :return: Merged dataframe.
    """
    final_df = None
    for csv_path in csv_files:
        # pd.read_csv seems to crash because of entries with backslashes, so this is a workaround
        with open(csv_path, 'r', encoding='UTF-8-sig', newline='') as csv_file:
            df = pd.DataFrame(csv.reader(csv_file, dialect="excel-backslash"))
            # Set first row as column names
            df.columns = df.iloc[0]
            df = df[1:]

            if final_df is None:
                final_df = df
            else:
                final_df = pd.concat([final_df, df], keys=primary_key, sort=False).drop_duplicates(subset=primary_key,
                                                                                                   keep="last")
    return final_df
