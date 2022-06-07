import os
from collections import defaultdict
from glob import glob

from create_visualization import generate_visualization
from mission_analysis_utils import csv_to_df, format_timestamp, convert_altitude, convert_position, sort_df


def perform_mission_analysis(flight_type):
    """
    To start mission analysis for the specified flight type
    :param flight_type: 0 refers to shorter mission and 1 refers to longer mission dataset
    :return: dash layout with configured chart
    """
    # dict holding available visualization
    type_dict = {
        0: "125068fc-f69b-4160-8f70-15ce5cbfdb80",
        1: "c59f300d-1004-480a-a1d0-fed04c525399"

    }
    messages_dict = defaultdict(list)
    try:
        # get the csv file paths(s)
        ulog_file_dict = read_ulog_input("dataset")
        for file_identifier, file_path_list in ulog_file_dict.items():
            if type_dict[flight_type] == file_identifier:
                messages_dict["file_identifier"] = [file_identifier]
                # check if the file name contains vehicle_gps_position
                trajectory_file_path = [s for s in file_path_list if "vehicle_gps_position" in s]
                if trajectory_file_path is not None:
                    # import trajectory data
                    df_trajectory = csv_to_df(trajectory_file_path[0])
                    # convert position
                    df_trajectory[["lat_converted", "lon_converted"]] = df_trajectory[["lat", "lon"]].apply(
                        convert_position)
                    df_trajectory['alt_converted'] = convert_altitude(df_trajectory["alt"])
                    df_trajectory['displayTime'] = format_timestamp(df_trajectory)
                    df_trajectory = sort_df(df_trajectory)
                    messages_dict["df_trajectory"] = df_trajectory

                # check if the file name contains airspeed
                airspeed_file_path = [s for s in file_path_list if "airspeed" in s]
                if airspeed_file_path is not None:
                    df_airspeed = csv_to_df(airspeed_file_path[0])
                    df_airspeed['displayTime'] = format_timestamp(df_airspeed)
                    df_airspeed = sort_df(df_airspeed)
                    messages_dict["df_airspeed"] = df_airspeed

                # check if the file name contains cpu load
                cpu_load_file_path = [s for s in file_path_list if "cpuload" in s]
                if cpu_load_file_path is not None:
                    df_cpu_load = csv_to_df(cpu_load_file_path[0])
                    df_cpu_load['displayTime'] = format_timestamp(df_cpu_load)
                    df_cpu_load = sort_df(df_cpu_load)
                    messages_dict["df_cpu_load"] = df_cpu_load

                # check if the file name contains air data
                vehicle_air_data_file_path = [s for s in file_path_list if "vehicle_air_data" in s]
                if vehicle_air_data_file_path is not None:
                    df_vehicle_air_data = csv_to_df(vehicle_air_data_file_path[0])
                    df_vehicle_air_data['displayTime'] = format_timestamp(df_vehicle_air_data)
                    df_vehicle_air_data = sort_df(df_vehicle_air_data)
                    messages_dict["df_vehicle_air_data"] = df_vehicle_air_data

                # check if the file name contains battery status
                battery_status_data_file_path = [s for s in file_path_list if "battery_status" in s]
                if battery_status_data_file_path is not None:
                    df_battery_status_data = csv_to_df(battery_status_data_file_path[0])
                    df_battery_status_data['displayTime'] = format_timestamp(df_battery_status_data)
                    df_battery_status_data = sort_df(df_battery_status_data)
                    messages_dict["df_battery_status_data"] = df_battery_status_data
        return generate_visualization(messages_dict)
    except ValueError as e:
        print("File processing conversion to dataframe failed: %s" % e)


def read_ulog_input(dataset_path):
    """
    To read ulog messages from the specified input folder. Currently it reads from dataset folder.
    :param dataset_path: ulog message path containing csv files
    :return: dict key as file identifier and value as list of csv files.
    """
    ulog_file_dict = {}
    try:
        # get all the csv file(s)
        ulog_csv_file = [file
                         for path, subdir, files in os.walk(dataset_path)
                         for file in glob(os.path.join(path, "*.csv"))]
        if len(ulog_csv_file) == 0:
            raise ValueError("No input messages available in the specified path")
        for ulog_csv_file in ulog_csv_file:
            # get individual filename
            ulog_file_name = os.path.basename(ulog_csv_file)
            # extract identifier
            ulog_file_identifier = ulog_file_name.split("_")
            # add identifier as key and csv file path as values
            if ulog_file_identifier[0] in ulog_file_dict:
                ulog_file_dict[ulog_file_identifier[0]].append(ulog_csv_file)
            else:
                ulog_file_dict[ulog_file_identifier[0]] = [ulog_csv_file]
    except ValueError as e:
        print('Exception during reading log messages: %s' % e)

    return ulog_file_dict
