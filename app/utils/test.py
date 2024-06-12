











































# import re
# from datetime import datetime

# def parse_datetime(data):
#     # Define a regex pattern for validation
#     pattern = r'^(\d{2}:\d{2}) (\d{2}:\d{2}) (\d{4}:\d{2}:\d{2})$'

#     # Validate the input format
#     match = re.match(pattern, data)
#     if not match:
#         return None

#     # Extract start time, end time, and date from the matched groups
#     start_time_str = match.group(1)
#     end_time_str = match.group(2)
#     date_str = match.group(3)

#     # Construct datetime objects
#     start_datetime = datetime.strptime(f'{date_str} {start_time_str}', '%Y:%m:%d %H:%M')
#     end_datetime = datetime.strptime(f'{date_str} {end_time_str}', '%Y:%m:%d %H:%M')

#     # Formatting datetime objects as strings
#     start_time = start_datetime.strftime('%Y:%m:%d %H:%M')
#     end_time = end_datetime.strftime('%Y:%m:%d %H:%M')

#     # Get timestamps
#     start_timestamp = start_datetime.timestamp()
#     end_timestamp = end_datetime.timestamp()

#     # Prepare dictionary
#     result = {
#         'start_timestr': start_time,
#         'start_timestamp': int(start_timestamp),
#         'start_datetime': start_datetime,
#         'end_timestr': end_time,
#         'end_timestamp': int(end_timestamp),
#         'end_datetime': end_datetime
#     }

#     return result

# # Example usage:
# data = '08:00 12:00 2024:6:12'
# parsed_data = parse_datetime(data)
# print(parsed_data)
