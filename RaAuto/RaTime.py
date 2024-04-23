from datetime import datetime, timedelta

def add_minutes(time_str, minutes):
    time = datetime.strptime(time_str, "%H:%M")
    updated_time = time + timedelta(minutes=minutes)
    return updated_time.strftime("%H:%M")