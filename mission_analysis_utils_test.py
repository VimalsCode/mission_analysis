import pandas as pd
import pytest

from mission_analysis_utils import csv_to_df, convert_altitude, format_timestamp


def test_df_conversion():
    df_result = csv_to_df(
        'test_dataset/test/125068fc-f69b-4160-8f70-15ce5cbfdb80_airspeed_0.csv')
    assert isinstance(df_result, pd.DataFrame)


def test_empty_filename():
    with pytest.raises(ValueError):
        csv_to_df('')


def test_altitude_conversion():
    assert convert_altitude(7522) == 7.522


def test_format_timestamp():
    df_test = pd.DataFrame([287721567, 290725766], columns=["timestamp"])
    test_data = ['00:04:47', '00:04:50']
    assert isinstance(format_timestamp(df_test), pd.Series)
    assert format_timestamp(df_test).all() == pd.Series(data=test_data, index=[0, 1], name='timestamp').all()


def test_format_timestamp_with_empty_df():
    df_test_empty = pd.DataFrame({'A': []})
    with pytest.raises(ValueError):
        format_timestamp(df_test_empty)
