#!/usr/bin/env python2
import datetime

import requests
import icalendar
import os

def set_mumble(event, start, end):
    import mice

    s = mice.murmur.getAllServers()[0]
    state = s.getChannelState(int(os.environ['CHANNEL_ID']))
    now = datetime.datetime.now()


    if event is not None:

        relname = None
        if start > now:
            timediff = start - now
            relname = "in {} minuten".format(timediff.total_seconds() // 60)
        else:
            timediff = end - now
            relname = "noch {} minuten".format(timediff.total_seconds() // 60)

        state.name = "[{}] Veranstaltung: {}".format(relname, event.decoded("summary"))
    else:
        state.name = "Veranstaltung: Keine Aktive Veranstaltung"

    s.setChannelState(state)

r = requests.get("https://das-labor.org/termine.ics")
data = r.text

cal = icalendar.Calendar.from_ical(data)

start_date = datetime.datetime.now() - datetime.timedelta(minutes=30)
end_date = datetime.datetime.now()

print("Checking between {} and {}".format(start_date, end_date))

selected_event = (None, None, None)

for event in cal.subcomponents:
    start = event.decoded("dtstart")
    end = event.decoded("dtend", None)
    if not isinstance(start, datetime.datetime):
        print("Warning: {} has no time set".format(event.decoded("summary")))
        start = datetime.datetime.combine(start, datetime.datetime.min.time())
    if end is None:
        end = start + datetime.timedelta(hours=2)

    if start > start_date and end < end_date:
        print("{} - {}: {}".format(start, end, event.decoded("summary")))
        selected_event = (event, start, end)


set_mumble(*selected_event)

