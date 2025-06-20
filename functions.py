
functions = [
    {
        "name": "check_free_slots",
        "description": "Check available meeting time slots on a specific date.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date to check availability. Format: YYYY-MM-DD"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Duration of the meeting in minutes. Default is 60.",
                    "default": 60
                }
            },
            "required": ["date"]
        }
    },
    {
        "name": "schedule_meeting",
        "description": "Schedule a meeting in the calendar.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Title or summary of the meeting."
                },
                "start_time": {
                    "type": "string",
                    "description": "Start time in ISO 8601 format (e.g., 2025-06-20T14:00:00)"
                },
                "end_time": {
                    "type": "string",
                    "description": "End time in ISO 8601 format (e.g., 2025-06-20T15:00:00)"
                },
                "attendees_emails": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "format": "email"
                    },
                    "description": "List of attendee email addresses."
                }
            },
            "required": ["summary", "start_time", "end_time"]
        }
    },
    {
        "name": "cancel_meeting",
        "description": "Cancel a scheduled calendar event by exact date and start time.",
        "parameters": {
            "type": "object",
            "properties": {
                "date_str": {
                    "type": "string",
                    "description": "Date of the event. Format: YYYY-MM-DD"
                },
                "time_str": {
                    "type": "string",
                    "description": "Time of the event. Format: HH:MM in 24-hour format"
                }
            },
            "required": ["date_str", "time_str"]
        }
    },
    {
        "name": "list_upcoming_meeting",
        "description": "List events scheduled for a specific date, optionally filtered by time.",
        "parameters": {
            "type": "object",
            "properties": {
                "date_str": {
                    "type": "string",
                    "description": "Date to fetch events from. Format: YYYY-MM-DD"
                },
                "time_str": {
                    "type": "string",
                    "description": "Optional time filter. Format: HH:MM in 24-hour format"
                }
            },
            "required": ["date_str"]
        }
    }
]
