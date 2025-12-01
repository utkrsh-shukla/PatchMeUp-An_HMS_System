from datetime import datetime, timedelta, date, time

def format_date(dt):
    return dt.strftime('%B %d, %Y') if dt and not isinstance(dt, str) else dt or ''

def format_time(t):
    return t.strftime('%I:%M %p') if t and not isinstance(t, str) else t or ''

def format_datetime(dt):
    return dt.strftime('%B %d, %Y %I:%M %p') if dt and not isinstance(dt, str) else dt or ''

def get_next_7_days():
    return [(date.today() + timedelta(days=i)) for i in range(7)]

def get_day_name(day_number):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day_number] if 0 <= day_number < 7 else ''

def generate_time_slots(start_time=time(9, 0), end_time=time(17, 0), interval_minutes=30):
    slots = []
    current = datetime.combine(date.today(), start_time)
    end_dt = datetime.combine(date.today(), end_time)
    
    while current < end_dt:
        slots.append(current.time())
        current += timedelta(minutes=interval_minutes)
    
    return slots
