import json

import plotly.graph_objects as go

from mission_analysis_utils import calculate_map_center

# outlier json
outlier_file = "outliers.json"


def generate_box_plot(df_data, fig_dict):
    """
    To generate the box plot for the provided dataframe and selected columns
    :param df_data: dataframe representing the geo temporal information
    :param fig_dict: dictionary with labels, names and title to be displayed
    :return: box plot figure
    """
    box_figure = go.Figure()
    box_figure.add_trace(
        go.Box(y=df_data[fig_dict['label_1']], name=fig_dict['name_1'], marker=dict(color='lightseagreen')))
    box_figure.add_trace(
        go.Box(y=df_data[fig_dict['label_2']], name=fig_dict['name_2'], marker=dict(color='darkgrey')))
    box_figure.update_layout(dict1=dict(
        title=fig_dict['title'],
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    ))
    return box_figure


def generate_scatter_plot(df_data, fig_dict, outlier=True, chart_type="altitude"):
    """
    To generate the scatter plot for provided dataframe and selected columns
    :param df_data: dataframe representing the geo temporal information
    :param fig_dict: dictionary with labels, names and title to be displayed
    :param outlier: to display outlier
    :param chart_type: type of chart
    :return: scatter plot figure
    """
    scatter_figure = go.Figure()
    scatter_figure.add_trace(go.Scatter(
        x=df_data[fig_dict['label_1_x']], y=df_data[fig_dict['label_1_y']],
        mode='lines',
        name=fig_dict['name_1']))
    scatter_figure.add_trace(go.Scatter(
        x=df_data[fig_dict['label_2_x']], y=df_data[fig_dict['label_2_y']],
        mode='lines',
        name=fig_dict['name_2']))
    if outlier and chart_type == "altitude":
        with open(outlier_file) as f:
            outlier_list = json.load(f)
            scatter_figure.add_trace(go.Scatter(
                x=df_data[fig_dict['label_1_x']][outlier_list], y=df_data[fig_dict['label_1_y']][outlier_list],
                mode='markers',
                name="outliers"))

    scatter_figure.update_layout(dict1=dict(
        title=fig_dict['title'],
        xaxis_title=fig_dict["xaxis_title"],
        yaxis_title=fig_dict["yaxis_title"]
    ))
    return scatter_figure


def generate_scatter_cpu_plot(df_data, fig_dict, outlier=True, chart_type="altitude"):
    """
    To generate the scatter plot for provided dataframe and selected columns
    :param df_data: dataframe representing the geo temporal information
    :param fig_dict: dictionary with labels, names and title to be displayed
    :param outlier: to display outlier
    :param chart_type: type of chart
    :return: scatter plot figure
    """
    scatter_figure = go.Figure()
    scatter_figure.add_trace(go.Scatter(
        x=df_data[fig_dict['label_1_x']], y=df_data[fig_dict['label_1_y']],
        mode='lines',
        name=fig_dict['name_1']))
    scatter_figure.add_trace(go.Scatter(
        x=df_data[fig_dict['label_2_x']], y=df_data[fig_dict['label_2_y']],
        mode='lines',
        name=fig_dict['name_2']))
    if outlier and chart_type == "altitude":
        with open(outlier_file) as f:
            outlier_list = json.load(f)
            scatter_figure.add_trace(go.Scatter(
                x=df_data[fig_dict['label_1_x']][outlier_list], y=df_data[fig_dict['label_1_y']][outlier_list],
                mode='markers',
                name="outliers"))

    scatter_figure.update_layout(dict1=dict(
        title=fig_dict['title'],
        xaxis_title=fig_dict["xaxis_title"],
        yaxis_title=fig_dict["yaxis_title"]
    ))
    return scatter_figure


def generate_alt_plot(df_trajectory, df_vehicle_air_data):
    """
    To generate altitude plot
    :param df_trajectory: dataframe with gps altitude
    :param df_vehicle_air_data: dataframe with barometer altitude
    :return: scatter plot figure
    """
    scatter_figure = go.Figure()
    scatter_figure.add_trace(go.Scatter(
        x=df_trajectory["displayTime"], y=df_trajectory["alt_converted"],
        mode='lines',
        name="gps altitude"))
    scatter_figure.add_trace(go.Scatter(
        x=df_vehicle_air_data["displayTime"], y=df_vehicle_air_data["baro_alt_meter"],
        mode='lines',
        name="barometer altitude"))
    scatter_figure.update_layout(dict1=dict(
        title="Altitude",
        xaxis_title="timestamp",
        yaxis_title="(m)"
    ))
    return scatter_figure


def generate_battery_plot(df_airspeed, df_battery_status_data):
    """
    To generate battery status plot
    :param df_airspeed: dataframe with airspeed
    :param df_battery_status_data: dataframe with battery status
    :return: scatter plot figure
    """
    scatter_figure = go.Figure()
    scatter_figure.add_trace(go.Scatter(
        x=df_airspeed["displayTime"], y=df_airspeed["air_temperature_celsius"],
        mode='lines',
        name="airspeed temperature"))
    scatter_figure.add_trace(go.Scatter(
        x=df_battery_status_data["displayTime"], y=df_battery_status_data["temperature"],
        mode='lines',
        name="battery temperature"))
    scatter_figure.update_layout(dict1=dict(
        title="Battery",
        xaxis_title="timestamp",
        yaxis_title=" "
    ))
    return scatter_figure


def generate_alt_box_plot(df_trajectory, df_vehicle_air_data):
    """
    To generate altitude box plot
    :param df_trajectory: dataframe with gps altitude
    :param df_vehicle_air_data: dataframe with barometer altitude
    :return: box plot figure
    """
    box_figure = go.Figure()
    box_figure.add_trace(
        go.Box(y=df_trajectory["alt_converted"], name="gps altitude", marker=dict(color='lightseagreen')))
    box_figure.add_trace(
        go.Box(y=df_vehicle_air_data["baro_alt_meter"], name="barometer altitude", marker=dict(color='darkgrey')))
    box_figure.update_layout(dict1=dict(
        title="Altitude data distribution",
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    ))
    return box_figure


def generate_trajectory_plot(df_data):
    """
    To plot the trajectories on the map
    :param df_data: dataframe with latitude and longitude in degrees
    :return: map with plotted latitude and longitude
    """
    # find the center of the map
    lon_center, lat_center = calculate_map_center(df_data)
    # plot the lat and lon
    trajectory_fig = go.Figure(data=go.Scattermapbox(
        lon=df_data['lon_converted'],
        lat=df_data['lat_converted'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        )))

    # map related properties
    trajectory_fig.update_layout(
        dict1=dict(title="Flight trajectory path"),
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            style="stamen-terrain",
            bearing=0,
            center=dict(
                lon=lon_center,
                lat=lat_center
            ),
            pitch=0,
            zoom=15
        ),
        mapbox_layers=[
            {
                'below': "traces",
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ],
    )
    return trajectory_fig
