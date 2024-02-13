from datetime import datetime


def get_date_time() -> str:
    """Get current date and time."""
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
