from __future__ import absolute_import

import decimal

import pytest

import pandas as pd

import ibis
import ibis.expr.datatypes as dt

import os


@pytest.fixture(scope='module')
def df():
    return pd.DataFrame({
        'plain_int64': list(range(1, 4)),
        'plain_strings': list('abc'),
        'plain_float64': [4.0, 5.0, 6.0],
        'plain_datetimes_naive': pd.Series(
            pd.date_range(start='2017-01-02 01:02:03.234', periods=3).values,
        ),
        'plain_datetimes_ny': pd.Series(
            pd.date_range(start='2017-01-02 01:02:03.234', periods=3).values,
        ).dt.tz_localize('America/New_York'),
        'plain_datetimes_utc': pd.Series(
            pd.date_range(start='2017-01-02 01:02:03.234', periods=3).values,
        ).dt.tz_localize('UTC'),
        'dup_strings': list('dad'),
        'dup_ints': [1, 2, 1],
        'float64_as_strings': ['100.01', '234.23', '-999.34'],
        'int64_as_strings': list(map(str, range(1, 4))),
        'strings_with_space': [' ', 'abab', 'ddeeffgg'],
        'int64_with_zeros': [0, 1, 0],
        'float64_with_zeros': [1.0, 0.0, 1.0],
        'strings_with_nulls': ['a', None, 'b'],
        'datetime_strings_naive': pd.Series(
            pd.date_range(start='2017-01-02 01:02:03.234', periods=3).values,
        ).astype(str),
        'datetime_strings_ny': pd.Series(
            pd.date_range(start='2017-01-02 01:02:03.234', periods=3).values,
        ).dt.tz_localize('America/New_York').astype(str),
        'datetime_strings_utc': pd.Series(
            pd.date_range(start='2017-01-02 01:02:03.234', periods=3).values,
        ).dt.tz_localize('UTC').astype(str),
        'decimal': list(map(decimal.Decimal, ['1.0', '2', '3.234'])),
        'array_of_float64': [[1.0, 2.0], [3.0], []],
        'array_of_int64': [[1, 2], [], [3]],
        'array_of_strings': [['a', 'b'], [], ['c']],
    })


@pytest.fixture(scope='module')
def batting_df():
    path = os.environ.get('BATTING_CSV', 'batting.csv')
    if not os.path.exists(path):
        pytest.skip('{} not found'.format(path))
    else:
        df = pd.read_csv(path, index_col=None, sep=',')
        num_rows = int(0.01 * len(df))
        return df.iloc[30:30 + num_rows].reset_index(drop=True)


@pytest.fixture(scope='module')
def awards_players_df():
    path = os.environ.get('AWARDS_PLAYERS_CSV', 'awards_players.csv')
    if not os.path.exists(path):
        pytest.skip('{} not found'.format(path))
    else:
        return pd.read_csv(path, index_col=None, sep=',')


@pytest.fixture(scope='module')
def df1():
    return pd.DataFrame(
        {'key': list('abcd'), 'value': [3, 4, 5, 6], 'key2': list('eeff')}
    )


@pytest.fixture(scope='module')
def df2():
    return pd.DataFrame(
        {'key': list('ac'), 'other_value': [4.0, 6.0], 'key3': list('fe')}
    )


@pytest.fixture(scope='module')
def client(df, df1, df2):
    return ibis.pandas.connect(
        {'df': df, 'df1': df1, 'df2': df2, 'left': df1, 'right': df2}
    )


@pytest.fixture(scope='module')
def t(client):
    return client.table(
        'df',
        schema={
            'decimal': dt.Decimal(4, 3),
            'array_of_float64': dt.Array(dt.double),
            'array_of_int64': dt.Array(dt.int64),
            'array_of_strings': dt.Array(dt.string),
        }
    )


@pytest.fixture(scope='module')
def lahman(batting_df, awards_players_df):
    return ibis.pandas.connect({
        'batting': batting_df,
        'awards_players': awards_players_df,
    })


@pytest.fixture(scope='module')
def left(client):
    return client.table('left')


@pytest.fixture(scope='module')
def right(client):
    return client.table('right')


@pytest.fixture(scope='module')
def batting(lahman):
    return lahman.table('batting')


@pytest.fixture(scope='module')
def awards_players(lahman):
    return lahman.table('awards_players')
