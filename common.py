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


def read_from_csv(csv_files):
    for csv_path in csv_files:
        # pd.read_csv seems to crash because of entries with backslashes, so this is a workaround
        with open(csv_path, 'r', encoding='UTF-8-sig', newline='') as csv_file:
            df = pd.DataFrame(csv.reader(csv_file, dialect="excel-backslash"))
            # Set first row as column names

            df.columns = df.iloc[0]
            df = df[1:]

            df.dropna(axis=1, inplace=True)  # Removes empty column sometimes added
        yield df


def join_df(dataframes, primary_key):
    """
    Open and left join successively csv files
    :param dataframes: A list of panda dataframes.
    :param primary_key: Primary key string used to match entries between themselves.
    :return: Merged dataframe.
    """
    final_df = None
    for df in dataframes:
        if final_df is None:
            final_df = df
        else:
            # final_df = final_df.join(df, on=primary_key)
            final_df = final_df.merge(df, on=primary_key, how='left')
    return final_df


def merge_update_df(dataframes, primary_key):
    """
    From multiple dataframes, apply them on top of each other.
    Based on primary key, matching entries are overridden while new ones are added.
    :param dataframes: A list of panda dataframes.
    :param primary_key: Primary key string used to match entries between themselves.
    :return: Merged dataframe.
    """
    final_df = None
    for df in dataframes:

        if final_df is None:
            final_df = df
        else:
            # FIXME Should support frames with not as many columns
            # If duplicates are generated, non-specified cells will be NaN by default
            # To avoid that we make sure that for each row df has, all data from final_df is present
            columns_provided_by_df = final_df.columns.intersection(df.columns).drop(primary_key)
            missing_data_df = final_df.drop(columns_provided_by_df, axis=1, errors="ignore")
            df = join_df([df, missing_data_df], primary_key=primary_key)
            final_df = pd.concat([final_df, df], keys=primary_key, sort=False).drop_duplicates(subset=primary_key,
                                                                                               keep="last")
    return final_df
