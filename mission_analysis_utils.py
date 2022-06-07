import numpy as np
import pandas as pd


def calculate_map_center(df_data):
    """
    given a dataframe with latitude and longitude, find the center
    :param df_data: dataframe containing latitude and longitude columns
    :return: longitude center and latitude center as float
    """
    if not df_data.empty:
        lon_center = (np.amin(df_data['lon_converted']) + np.amax(df_data['lon_converted'])) / 2
        lat_center = (np.amin(df_data['lat_converted']) + np.amax(df_data['lat_converted'])) / 2
        return lon_center, lat_center


def sort_df(df_data):
    """
    given a dataframe perform sort operation based on timestamp attribute
    :param df_data: dataframe containing timestamp colum
    :return: sorted dataframe
    """
    df_data.sort_values(by="timestamp", inplace=True)
    df_data.reset_index(inplace=True)
    return df_data


def convert_position(position):
    """
    convert geo position to degree
    :param position: Latitude and Longitude in 1E-7 degrees
    :return:converted position
    """
    return position / 1e7


def format_timestamp(df_data):
    """
    To convert timestamp in microsecond to display format
    :param df_data: dataframe with timestamp column
    :return:specified format applied to the dataframe
    """
    if df_data.empty:
        raise ValueError("dataframe is empty")
    # return  pd.to_datetime(df_data['timestamp'], unit='us').dt.time
    return pd.to_datetime(df_data["timestamp"], unit='us').dt.strftime("%H:%M:%S")


def csv_to_df(file_name):
    """
    To read the csv file from the specified location
    :param file_name: ulog message file name
    :return: csv file converted to pandas dataframe
    """

    if len(file_name) == 0:
        raise ValueError("Filename is empty")
    return pd.read_csv(file_name)


def convert_altitude(altitude):
    """
    To perform altitude conversion to meter
    :param altitude: Altitude in millimetres
    :return:altitude in m
    """
    return altitude / 1000
