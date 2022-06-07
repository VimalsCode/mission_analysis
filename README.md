# Mission Log Analysis and visualization

## Overview

This project provides mechanism to help understand a flight mission based on the recorded data log and communicates the
mission general information to provide a starting point about the mission.

## Message schema

The project relies on the [PX4 log message](https://docs.px4.io/master/en/dev_log/ulog_file_format.html) format. These
are the following
messages used for the analysis,

* Airspeed message
  - [Airspeed](https://github.com/PX4/PX4-Autopilot/blob/0595efbd9b7f0c9746132b523e71fc0f4d666c90/msg/airspeed.msg)
* Vehicle GPS Position
  - [Vehicle GPS](https://github.com/PX4/PX4-Autopilot/blob/0595efbd9b7f0c9746132b523e71fc0f4d666c90/msg/vehicle_gps_position.msg)
* Vehicle Air Data
  - [Vehicle Air Data](https://github.com/PX4/PX4-Autopilot/blob/0595efbd9b7f0c9746132b523e71fc0f4d666c90/msg/vehicle_air_data.msg)
* CPU Load message
  - [CPU Load](https://github.com/PX4/PX4-Autopilot/blob/0595efbd9b7f0c9746132b523e71fc0f4d666c90/msg/cpuload.msg)
* Battery Status
  - [Battery status](https://github.com/PX4/PX4-Autopilot/blob/0595efbd9b7f0c9746132b523e71fc0f4d666c90/msg/battery_status.msg)

## Platform information

The PX4 Log message is downloaded for the following platform from [here] (https://review.px4.io/browse).

* [Generic quad delta VTOL Standard VTOL (13006)](https://review.px4.io/plot_app?log=c59f300d-1004-480a-a1d0-fed04c525399)
  - 29-03-2020 09:09 - Referred as platform 0
* [Generic Quadplane VTOL Standard VTOL (13000)](https://review.px4.io/plot_app?log=125068fc-f69b-4160-8f70-15ce5cbfdb80)
  - 08-05-2022 08:49 - Referred as platform 1

## Project Set Up and Installation

### Step 1: Clone/Unzip the project

The project is provided as zip file. This project is tested against Python 3.9 and it
requires an internet connection
for the map display.

### Step 2: Setup environment and install dependencies in Linux environment

* create a virtual environment using the following command,

```
python -m venv <env-name>
```

* Use the following command to activate the virtual environment,

```
source <env-name>/bin/activate
```

* Required project dependencies can be installed based on the following command,

```
pip3 install -r requirements.txt
```

### Step 3: To run the application

To run the application use the following command,

```
python main.py -t 0 or 1
``` 

Application visualization is running on http://localhost:8050/

Overview about the commandline parameters is provided here,
Optional Parameters - visualization related:

|Parameter name  | Description |
| ------------- | ------------- |
| -t, --type | To specify the platform type for visualization (default=0)  |

## Documentation

The project contains the following file structure

| File name                                                                                            | Description                                                                                                  |
|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Airspeed_Cluster_Analysis.html                                                                       | The notebook contains the executed code and clustering based on DBSCAN method                                |
| Airspeed_Cluster_Analysis.ipynb                                                                      | The notebook contains the necessary code to perform DBSCAN analysis and identifier outlier labels            |
| assets folder                                                                                        | This folder contains visualization CSS                                                                       |
| dataset folder                                                                                       | This folder contains converted CSV files based on ULog messages                                              |
| test_dataset folder                                                                                  | This folder contains converted CSV files based on ULog messages used during unit test                        |
| main.py                                                                                              | Main python program to start the analysis and visualization. It currently supports one command line argument |
| input_processor.py,<br/>mission_analysis_utils.py<br/>create_visualization.py<br/>chart_generator.py | These set of files contains logic for dataframe creation, data preprocessing and visualization creation      |
| outlier.json                                                                                         | Detected outlier label index from DBSCAN is stored here                                                      |