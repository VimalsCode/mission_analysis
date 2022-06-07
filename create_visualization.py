from dash import dcc
from dash import html

from chart_generator import generate_box_plot, generate_scatter_plot, generate_trajectory_plot, generate_alt_plot, \
    generate_alt_box_plot, generate_battery_plot


def generate_visualization(messages_dict):
    """
    To generate dash chart for the selected messages
    :param messages_dict: dict containing message(airspeed/cpu load) as key and value as dataframe generated from ulog
    message
    :return: dash generated layout
    """
    if messages_dict:
        # trajectory
        trajectory_fig = generate_trajectory_plot(messages_dict['df_trajectory'])
        # airspeed
        airspeed_dict = {
            "label_1_x": "displayTime",
            "label_1_y": "indicated_airspeed_m_s",
            "name_1": "indicated_airspeed",
            "label_2_x": "displayTime",
            "label_2_y": "true_airspeed_m_s",
            "name_2": "true_airspeed",
            "title": "Airspeed",
            "xaxis_title": "timestamp",
            "yaxis_title": "m/s"
        }
        # to display outlier from cluster algorithm
        if "125068fc-f69b-4160-8f70-15ce5cbfdb80" in messages_dict['file_identifier']:
            airspeed_chart_figure = generate_scatter_plot(messages_dict['df_airspeed'], airspeed_dict, outlier=True)
        else:
            airspeed_chart_figure = generate_scatter_plot(messages_dict['df_airspeed'], airspeed_dict, outlier=False)

        # airspeed outlier
        airspeed_outlier_dict = {
            "label_1": "indicated_airspeed_m_s",
            "name_1": "indicated",
            "label_2": "true_airspeed_m_s",
            "name_2": "true",
            "title": "Airspeed data distribution"
        }
        airspeed_box_figure = generate_box_plot(messages_dict['df_airspeed'], airspeed_outlier_dict)

        # cpu
        cpu_load_dict = {
            "label_1_x": "displayTime",
            "label_1_y": "load",
            "name_1": "cpu_load",
            "label_2_x": "displayTime",
            "label_2_y": "ram_usage",
            "name_2": "ram_usage",
            "title": "CPU and RAM load",
            "xaxis_title": "timestamp",
            "yaxis_title": ""
        }
        cpu_chart_figure = generate_scatter_plot(messages_dict['df_cpu_load'], cpu_load_dict, outlier=False)

        # cpu outlier
        cpu_outlier_dict = {
            "label_1": "load",
            "name_1": "cpu_load",
            "label_2": "ram_usage",
            "name_2": "ram_usage",
            "title": "Load data distribution"
        }
        cpu_box_figure = generate_box_plot(messages_dict['df_cpu_load'], cpu_outlier_dict)
        # altitude chart
        alt_chart_figure = generate_alt_plot(messages_dict['df_trajectory'], messages_dict['df_vehicle_air_data'])
        alt_box_figure = generate_alt_box_plot(messages_dict['df_trajectory'], messages_dict['df_vehicle_air_data'])
        # battery temperature
        battery_chart_figure = generate_battery_plot(messages_dict['df_airspeed'],
                                                     messages_dict['df_battery_status_data'])

        # create layout for the visualization
        layout = html.Div(children=[
            html.Div(
                children=[
                    html.H1(
                        children='Post Flight Mission Analysis',
                        className="header-title"
                    ),
                    html.P(
                        children="Based on PX4 Log data",
                        className="header-description"
                    )
                ],
                className="header"
            ),

            html.Div(children=[
                # trajectory figure
                html.Div(
                    children=dcc.Graph(id="trajectory", figure=trajectory_fig),
                    className="card"),
                # airspeed figure
                html.Div(children=dcc.Graph(
                    id="AirSpeedGraph",
                    figure=airspeed_chart_figure
                ), className="card"),
                # outlier airspeed
                html.Div(children=dcc.Graph(
                    id="AirSpeedGraphOutlier",
                    figure=airspeed_box_figure
                ), className="card"),
                # cpu load figure
                html.Div(children=dcc.Graph(
                    id="CpuLoadGraph",
                    figure=cpu_chart_figure
                ), className="card"),
                # outlier cpu
                html.Div(children=dcc.Graph(
                    id="CpuLoadGraphOutlier",
                    figure=cpu_box_figure
                ), className="card"),
                # altitude figure
                html.Div(children=dcc.Graph(
                    id="Altitude",
                    figure=alt_chart_figure
                ), className="card"),
                # outlier alt
                html.Div(children=dcc.Graph(
                    id="AltGraphOutlier",
                    figure=alt_box_figure
                ), className="card"),
                # battery usage
                html.Div(children=dcc.Graph(
                    id="Battery",
                    figure=battery_chart_figure
                ), className="card")
            ],
                className="wrapper"

            )

        ])
        return layout
    else:
        raise ValueError("Does not have required dataframe(s) for generating visualization")
