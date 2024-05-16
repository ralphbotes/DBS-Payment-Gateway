def dbs_timestamp(date_obj, type=1):
    # Get year, month, and day in "yyyymmdd" format
    year = str(date_obj.year)
    month = str(date_obj.month).zfill(2)
    day = str(date_obj.day).zfill(2)
    date_str = f"{year}-{month}-{day}" if type == 1 else f"{year}{month}{day}"

    # Get hours, minutes, seconds, and milliseconds in "hh:mm:ss.mss" format
    hours = str(date_obj.hour).zfill(2)
    minutes = str(date_obj.minute).zfill(2)
    seconds = str(date_obj.second).zfill(2)
    milliseconds = str(date_obj.microsecond // 1000).zfill(3)
    time_str = f"{hours}:{minutes}:{seconds}.{milliseconds}" if type == 1 else f"{hours}{minutes}{seconds}{milliseconds}"

    # Combine date and time into the final format
    return f"{date_str}T{time_str}" if type == 1 else f"{date_str}{time_str}"  # Output: "2021-02-14T15:07:26.222"