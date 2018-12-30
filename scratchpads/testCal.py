from ics import Calendar
from datetime import datetime
import requests    # Alternative: use requests
from logons import calendar_url

c = Calendar(requests.get(calendar_url).text)
today = datetime.today().date()
in_london = any([event.begin.date() == today for event in c.events])

print(in_london)
