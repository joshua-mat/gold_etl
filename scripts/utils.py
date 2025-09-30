import re
from datetime import datetime

def format_date(raw_date):
    cleaned_date = re.sub(r'(st|nd|rd|th)', '', raw_date)
    cleaned_date = cleaned_date.replace("Sept", "Sep")
    # Parse to datetime
    date_obj = datetime.strptime(cleaned_date.strip(), "%d %b %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date
