import math
import numpy as np
import pandas as pd
from io import StringIO

from user_variables import *

# Global DataFrame to store GPS data
gps_data_accumulated = None
current_index = 0


# Function definitions

# 1.0 Initialize the data to be used for calculation.

def data_frame(stream):
    """
    Append GPS data from a string containing CSV data to a global DataFrame and return it.

    Parameters:
    stream (str): A string containing the CSV data of the GPS data.

    Returns:
    pandas.DataFrame: A DataFrame containing the accumulated GPS data.
    """
    global gps_data_accumulated, current_index

    stream_data = StringIO(stream)
    new_data = pd.read_csv(stream_data, delimiter=',', header=None)
    headers = ['timestamp','latitude','longitude','direction','vehicle_motion_status','speed_mph','acceleration_from_gps_speed']
    # headers = ['timestamp', 'direction', 'speed_mph']
    new_data.columns = headers

    # Add an index column to the new data
    new_data['index'] = range(current_index, current_index + len(new_data))
    current_index += len(new_data)  # Update the global index counter

    if gps_data_accumulated is None:
        gps_data_accumulated = new_data
    else:
        # Keep only the last row of the existing data and append the new data
        gps_data_accumulated = pd.concat(
            [gps_data_accumulated.iloc[-1:], new_data], ignore_index=True)

    # Reset the index to align with the 'index' column
    gps_data_accumulated.reset_index(drop=True, inplace=True)

    return gps_data_accumulated


# 2. Calculate the difference in heading per second
def angular_distance(angle1, angle2):
    """
    Calculate the angular distance between two angles.

    Parameters:
    angle1 (float): The first angle in degrees.
    angle2 (float): The second angle in degrees.

    Returns:
    float: The angular distance between the two angles in radians.
    """
    angle1 = angle1 % 360.0
    angle2 = angle2 % 360.0

    distance = abs(angle1 - angle2)
    distance = min(distance, 360.0 - distance)
    if angle1 > angle2:
        return distance * (np.pi/180)
    else:
        return -distance * (np.pi/180)


# 3.0 Estimates the Radius of curve as the truck turns or changes heading
def find_curve_radius(angle_radians, truck_length=truck_length):
    """
    Calculate the radius of the circle formed by the given angle and truck length.

    Parameters:
    angle_radians (float): The angle in radians.
    truck_length (float): The length of the truck in meters.

    Returns:
    float: The radius of the circle in meters. Returns positive infinity for edge cases.
    """

    # Validate input parameters
    if not isinstance(angle_radians, (int, float)):
        raise ValueError("The angle must be a number (int or float).")

    if not isinstance(truck_length, (int, float)) or truck_length <= 0:
        raise ValueError(
            "Truck length must be a positive number (int or float).")

    # Handle edge cases for angle being 0 or π radians
    if math.isclose(angle_radians, 0, abs_tol=1e-9) or math.isclose(angle_radians, math.pi, abs_tol=1e-9):
        return float('inf')

    # Calculate the radius
    radius = truck_length / (math.tan(angle_radians) + 1e-5)

    return np.abs(radius)


# 4.0 Estimate the height of center of gravity of the truck based on truck type and loading conditions.
def height_of_center_of_gravity(mass_truckhead, mass_reeftrailor,
                                height_of_center_of_gravity_truckhead,
                                height_of_center_of_gravity_trailer):
    """
    Calculate the combined height of the center of gravity for a truck and its trailer.

    Parameters:
    mass_truckhead (float): The mass of the truck head in kilograms.
    mass_reeftrailor (float): The mass of the reef trailer in kilograms.
    height_of_center_of_gravity_truckhead (float): The height of the truck head's center of gravity in meters.
    height_of_center_of_gravity_trailer (float): The height of the trailer's center of gravity in meters.

    Returns:
    float: The combined height of the center of gravity for the truck and trailer in meters.
    """
    h_cm = ((mass_truckhead * height_of_center_of_gravity_truckhead) +
            (mass_reeftrailor * height_of_center_of_gravity_trailer)) / \
        (mass_truckhead + mass_reeftrailor)

    return h_cm


# Calculate the combined height of the center of gravity for the truck and trailer
h_cm = height_of_center_of_gravity(mass_truckhead,
                                    mass_reeftrailor,
                                    height_of_center_of_gravity_truckhead,
                                    height_of_center_of_gravity_trailer)


# 5.0 Estimates the threshold speed at which the truck must travel for a given Radius or turn
# and type of truck, it's height of center of gravity (loading conditions).
def critical_speed(r, h_cm=h_cm, semi_trackwidth=semi_trackwidth):
    """
    Calculate the critical speed for a given radius, height, and semi track width.

    Parameters:
    r (float): The radius of the turn in meters.
    h_cm (float): The height of the vehicle's center of mass in meters.
    semi_trackwidth (float): The semi track width of the vehicle in meters.

    Returns:
    float: The critical speed in miles per hour.

    Raises:
    ValueError: If the input parameters are not of the expected type or are non-positive.
    """

    # # Validate input parameters
    # if not all(isinstance(param, (int, float)) and param > 0 for param in [r, h_cm, semi_trackwidth]):
    #     raise ValueError(
    #         "All parameters must be positive numbers (int or float).")

    # Constants
    g = 9.81  # Acceleration due to gravity in m/s^2
    METER_PER_SECOND_TO_MILES_PER_HOUR = 2.23694  # Conversion factor

    # Calculate critical speed in meters per second
    crit_speed = np.sqrt((g * semi_trackwidth) / (2 * h_cm) * r)

    # Convert to miles per hour
    critical_speed_mph = crit_speed * METER_PER_SECOND_TO_MILES_PER_HOUR

    return critical_speed_mph



