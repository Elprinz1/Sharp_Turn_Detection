# Sharp Turn Detection Using GPS Data

Accidents involving commercial trucks can have devastating consequences, both in terms of human lives and financial implications. According to the Federal Motor Carrier Safety Administration (FMCSA), the estimated average accident costs for semi-trucks are $91,000, with average injury costs around $334,892 and average fatal accident settlements exceeding $7.2 million. Given these staggering figures, prioritizing safety measures is paramount for truckers and fleet management companies.

This project addresses the critical need for accident prevention by leveraging GPS data to detect sharp turns made by semi-trucks. By employing rule-based & advanced machine learning techniques, the provided Python code processes GPS data, meticulously analyzing the trucks's movements to identify instances of sharp turns based on significant changes in direction over time. 

## Getting Started

### Prerequisites

Ensure you have Python installed on your machine along with the following libraries:

- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn`
- `imbalanced-learn`

You can install these dependencies using pip:

```bash
pip install numpy pandas matplotlib scikit-learn imbalanced-learn
```

## Installation

1. Clone the repository to your local machine.
2. Ensure all dependencies listed above are installed.
3. Place your GPS data CSV file in the project directory.

## Data Format

Your GPS data should be in a CSV format with the following columns:

- `timestamp`: The date and time of the GPS reading.
- `latitude`: The latitude coordinate.
- `longitude`: The longitude coordinate.
- `direction`: The direction the vehicle is moving in degrees.
- `vehicle_motion_status`: Indicates if the vehicle is moving or stationary.
- `speed_mph`: The speed of the vehicle in miles per hour.
- `acceleration_from_gps_speed`: The acceleration value derived from GPS speed.

## Usage

1. Load your GPS data using the `data_frame` function by passing the CSV file content as a string.
2. Utilize the provided functions to analyze the data:
    - `date_time` converts timestamp strings to total seconds.
    - `angular_distance` calculates the angular distance between two headings.
    - `aggregate_heading_time` groups the data and calculates the change in heading over time.
3. Additional functions like `height_of_center_of_gravity` and `critical_speed` are provided for more in-depth analysis.
4. Identify sharp turns based on significant changes in direction over short time intervals.


# Load the data
stream = 'path_to_your_csv_data'
df = data_frame(stream)

# Analyze the data for sharp turns
aggregated_df = aggregate_heading_time(df)
# Further analysis can be done based on the aggregated data

