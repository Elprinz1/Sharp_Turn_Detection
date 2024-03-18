import time, csv, schedule
from utils import *
from sendmail import *


def checkForSharpTurnEvent(stream):
    gps_df = data_frame(stream)

     # Check if the DataFrame has at least two rows
    if gps_df is not None and len(gps_df) >= 2:

        # Convert 'timestamp' to datetime object
        gps_df['timestamp'] = pd.to_datetime(gps_df['timestamp'])

        # Calculate the angular distance between consecutive headings
        gps_df['previous_heading'] = gps_df['direction'].shift()
        gps_df['angular_distance'] = gps_df.apply(lambda row: angular_distance(
            row['previous_heading'], row['direction']), axis=1)

        # Convert speed from miles per hour to meters per second
        gps_df['speed_mps'] = gps_df['speed_mph']*.44704

        # Calculate the radius of the circle formed by the angular distance and truck length
        gps_df['radius'] = gps_df['angular_distance'].apply(find_curve_radius)

        
        # Calculate the critical speed for each radius
        gps_df['critical_speed'] = gps_df['radius'].apply(critical_speed)

        # Determine if the speed is greater than the critical speed
        gps_df['result'] = np.where(
            gps_df.critical_speed <= gps_df['speed_mph'], 1, 0)
        
        print(gps_df)

        # Return boolean value if the truck is in a sharp turn--[store metadata in seperate file]
        # append the data to a csv file
        if gps_df.result.iloc[-1] == 1:
            signal = 'Sharp turn detected!!!'
            metadata = {
                'Timestamp': gps_df.timestamp.iloc[-1],
                'Previous Heading': gps_df.previous_heading.iloc[-1],
                'Current Heading': gps_df.direction.iloc[-1],
                'Change in Heading (C)': round(gps_df.angular_distance.iloc[-1] * (180/np.pi), 1),
                'Speed': gps_df.speed_mph.iloc[-1],
                'SharpTurn': 'True'

            }
            print(signal)
            print(metadata)

            # Append metadata to the CSV file
            with open(csv_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=metadata.keys())
                if f.tell() == 0:  # Check if the file is empty
                    writer.writeheader()
                writer.writerow(metadata)
            

            # Send metadata to Email
            recipients = ['email_1', 'email_2', 'email_3', 'email_4']
            # for recipient in recipients:
            send_email(recipients, f'Sharp Turn detected with the following details :)\n\n {metadata} \n\nRegards, \n<Your Name>')

            return signal, metadata
        
        

    else:
    # Handle case where there are not enough rows in the DataFrame
        print("Not enough rows for processing sharp turn event.")
        # pass
        return None, None
    

def onTimeChanged():
    timestamp = timestamp
    latitude = latitude
    longitude = longitude
    direction = direction
    vehicle_motion_status = vehicle_motion_status
    speed_mph = speed_mph
    acceleration_from_gps_speed = acceleration_from_gps_speed
    
    # Create a CSV string
    csv_string = f"{timestamp},{latitude},{longitude},{direction},{vehicle_motion_status},{speed_mph},{acceleration_from_gps_speed}\n"

    # Call the function with the CSV string
    checkForSharpTurnEvent(csv_string)

def testRun():
    # Load the data from the CSV file into a dataframe (df)
    stream_data = '<Path to csv file>'  # takes a batch of stream data after 1s

    # Open the CSV file as a stream
    with open(stream_data, 'r') as stream:
        for line in stream:
            # Process the line
            checkForSharpTurnEvent(line)

            # Introduce a delay of 1 second
            time.sleep(1)


if __name__ == '__main__':
    csv_path = './logic_result.csv'

    # schedule.every(1).seconds.do(onTimeChanged, location='location object')
    schedule.every(1).seconds.do(testRun)

    while True:
        schedule.run_pending()
        # time.sleep(1)

        

