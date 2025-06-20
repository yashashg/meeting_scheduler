import datetime
from calendar_auth import get_calendar_service
from datetime import datetime, timedelta, time, timezone,date
from dateutil.parser import parse

service = get_calendar_service()

def check_free_slots(date: str, duration_minutes=60):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    # Working hours (9 AM to 6 PM) 
    working_start = datetime.combine(date_obj, time(9, 0, tzinfo=timezone.utc))
    working_end = datetime.combine(date_obj, time(18, 0, tzinfo=timezone.utc))
    events_result = service.events().list(
        calendarId='primary',
        timeMin=working_start.isoformat(),
        timeMax=working_end.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    # Function to find gaps between events
    def get_available_slots(events, start_time, end_time, duration_minutes):
        events.sort(key=lambda e: e['start'].get('dateTime', e['start'].get('date')))
        slots = []
        cursor = start_time
        for event in events:
            try:
                start_str = event['start']['dateTime']
                end_str = event['end']['dateTime']
                event_start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                event_end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            except KeyError:
                continue  # skip all-day or invalid events

            # Find gaps
            if event_start > cursor:
                while cursor + timedelta(minutes=duration_minutes) <= event_start:
                    slot_end = cursor + timedelta(minutes=duration_minutes)
                    slots.append((cursor.strftime('%I:%M %p'), slot_end.strftime('%I:%M %p')))
                    cursor = slot_end
            if event_end > cursor:
                cursor = event_end
        # Fill end-of-day gaps
        while cursor + timedelta(minutes=duration_minutes) <= end_time:
            slot_end = cursor + timedelta(minutes=duration_minutes)
            slots.append((cursor.strftime('%I:%M %p'), slot_end.strftime('%I:%M %p')))
            cursor = slot_end

        return slots

    return get_available_slots(events, working_start, working_end, duration_minutes)

def schedule_meeting(summary, start_time, end_time, attendees_emails=[]):
    # Parse input times
    print(summary, start_time, end_time, attendees_emails)

    start_time = start_time+"+05:30"
    end_time = end_time+"+05:30"
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
        'attendees': [{'email': email} for email in attendees_emails]
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('status')

def cancel_meeting(date_str: str, time_str: str) -> str:
    try:
        print(f"Using calendar service: {service}")
        # Parse date and time
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        input_time = datetime.strptime(time_str, "%H:%M").time()

        # Define time range for that day
        day_start = date_obj.replace(hour=0, minute=0, second=0)
        day_end = date_obj.replace(hour=23, minute=59, second=59)

        events_result = service.events().list(
            calendarId='primary',
            timeMin=day_start.isoformat() + 'Z',
            timeMax=day_end.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Look for exact time match
        for event in events:
            if 'dateTime' in event['start']:
                event_dt = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                if event_dt.hour == input_time.hour and event_dt.minute == input_time.minute:
                    # Match found — cancel
                    service.events().delete(calendarId='primary', eventId=event['id']).execute()
                    return f" Event '{event.get('summary', 'Untitled')}' on {date_str} at {time_str} cancelled."

        return f" No event found at {time_str} on {date_str} to cancel."

    except Exception as e:
        return f" Error cancelling event: {str(e)}"


def list_upcoming_meeting(date_str="", time_str=""):

    if not date_str:
        return "Please provide at least a date (in YYYY-MM-DD format)."

    try:
        # Parse date
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        time_min = date_obj.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        time_max = date_obj.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

        # Fetch all events for the day
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        # If time also provided, match exact hour + minute manually
        if time_str:
            input_time = datetime.strptime(time_str, "%H:%M").time()

            matched_events = []
            for event in events:
                if 'dateTime' in event['start']:
                    event_time = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00')).time()
                    if event_time.hour == input_time.hour and event_time.minute == input_time.minute:
                        
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        end = event['end'].get('dateTime', event['end'].get('date'))
                        matched_events.append({
                            'summary': event.get('summary', 'No Title'),
                            'start': start,
                            'end': end,
                            'attendees': [attendee.get('email') for attendee in event.get('attendees', [])]
                        })

            if not matched_events:
                return f" No events found at {time_str} on {date_str}."
            return  matched_events

        # Only date case — return all events on that day
        if not events:
            return f"No events found on {date_str}."
        # Format events for output
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            formatted_events.append({
                'summary': event.get('summary', 'No Title'),
                'start': start,
                'end': end,
                'attendees': [attendee.get('email') for attendee in event.get('attendees', [])]
            })
        return formatted_events

    except Exception as e:
        return f"Error: {str(e)}"
