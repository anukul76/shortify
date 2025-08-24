from datetime import datetime, timezone
from typing import Union

class DateTimeUtil:
    
    
    @staticmethod
    def get_current_timestamp() -> datetime:
        
        return datetime.now(timezone.utc)
    
    @staticmethod
    def get_current_timestamp_tz() -> datetime:
        
        return datetime.now(timezone.utc)
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        
        return datetime.strptime(date_str, format_str)
    
    @staticmethod
    def is_valid_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
        
        if not date_str or not isinstance(date_str, str):
            return False
        try:
            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def to_iso_format(dt: datetime) -> str:
        
        return dt.isoformat()
    
    @staticmethod
    def from_iso_format(iso_string: str) -> datetime:
        
        return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    
    @staticmethod
    def to_timestamp(dt: datetime) -> int:
        
        return int(dt.timestamp())
    
    @staticmethod
    def from_timestamp(timestamp: Union[int, float]) -> datetime:
        
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        
        from datetime import timedelta
        return dt + timedelta(days=days)
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        
        from datetime import timedelta
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        
        from datetime import timedelta
        return dt + timedelta(minutes=minutes)
    
    @staticmethod
    def get_start_of_day(dt: datetime) -> datetime:
        
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_end_of_day(dt: datetime) -> datetime:
        
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def get_days_between(start_date: datetime, end_date: datetime) -> int:
        
        return (end_date - start_date).days
    
    @staticmethod
    def get_hours_between(start_date: datetime, end_date: datetime) -> float:
        
        return (end_date - start_date).total_seconds() / 3600
    
    @staticmethod
    def is_past(dt: datetime) -> bool:
        
        return dt < datetime.utcnow()
    
    @staticmethod
    def is_future(dt: datetime) -> bool:
        
        return dt > datetime.utcnow()
    
    @staticmethod
    def format_relative_time(dt: datetime, now: datetime = None) -> str:
        
        if now is None:
            now = datetime.utcnow()
        diff = now - dt
        
        if diff.total_seconds() > 0:
            # Past time
            if diff.days > 0:
                return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                return f"{diff.seconds} second{'s' if diff.seconds != 1 else ''} ago"
        else:
            # Future time
            future_diff = dt - now
            if future_diff.days > 0:
                return f"in {future_diff.days} day{'s' if future_diff.days != 1 else ''}"
            elif future_diff.seconds > 3600:
                hours = future_diff.seconds // 3600
                return f"in {hours} hour{'s' if hours != 1 else ''}"
            elif future_diff.seconds > 60:
                minutes = future_diff.seconds // 60
                return f"in {minutes} minute{'s' if minutes != 1 else ''}"
            else:
                return "just now"