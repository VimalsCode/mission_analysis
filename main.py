import argparse

import dash

from input_processor import perform_mission_analysis

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet"
    }

]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Post flight analysis"
server = app.server


def parse_args():
    parser = argparse.ArgumentParser(description="Launch a Mission Analysis application.")
    parser.add_argument("-t", "--type", type=int, default=0,
                        help="choose platform type (0 or 1)")
    args = parser.parse_args()
    return args.type


# identify the platform type. Currently, two type is possible
visualization_type = parse_args()

# generate the visualization
try:
    app.layout = perform_mission_analysis(visualization_type)
except ValueError as e:
    print("Layout creation can not be generated at the moment: %s" % e)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
