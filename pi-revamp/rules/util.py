from datetime import datetime


def is_daytime(current_time: datetime) -> bool:
    return current_time.hour >= 9 and current_time.hour < 21
