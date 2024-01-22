def convert_time_to_seconds(time):
    splitted_time = time.split(":")
    
    minutes = int(splitted_time[0])
    seconds = int(splitted_time[1])
    
    fixed_time = (minutes * 60) + seconds
    
    return fixed_time