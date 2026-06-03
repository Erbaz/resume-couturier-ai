from datetime import datetime
from zoneinfo import ZoneInfo

def get_la_start_of_day() -> datetime:
    """Returns the start of the current day (00:00:00) in Los Angeles time."""
    tz = ZoneInfo("America/Los_Angeles")
    now_la = datetime.now(tz)
    return datetime(now_la.year, now_la.month, now_la.day, tzinfo=tz)