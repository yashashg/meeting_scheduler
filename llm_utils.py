import openai
import json
import getpass
import os
from functions import functions
from calendar_code import check_free_slots, schedule_meeting, cancel_meeting, list_upcoming_meeting
from datetime import datetime

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# 🧠 Memory buffer (chat history)
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M")


system_prompt = f"""
You are Smart Scheduler, a voice-based AI assistant that helps users manage their Google Calendar.
You assist with: Scheduling new meetings,Checking available slots,Listing meetings,Canceling meetings
Today's date is {current_date}, and current time is {current_time} — use this for all "today", "now", or "tomorrow" references.
Engage in multi-turn, context-aware conversations. Always clarify missing info like:
Meeting date, time, duration, Title (summary),Attendees emails , Cancellation confirmations or scheduling conflicts

Handle complex queries:
Deadlines (e.g., “before my flight on Friday at 6 PM”)
Relative dates (e.g., “2 days after Project Kickoff”)
Vague time (“evening”, “usual sync-up”)
Conflicts (suggest alternatives if slot is taken)

When all details are available, call the appropriate function silently.
Never guess — ask if unsure.
Respond in short, natural, and warm assistant-style replies — ideal for voice (TTS). Examples:
“Got it. Let me check.”
“Just a moment.”
“Would you like to invite anyone else?”
“Here are the options.”
Be precise with date/time formats and always summarize outcomes clearly.
"""

function_map = {
    "check_free_slots": check_free_slots,
    "schedule_meeting": schedule_meeting,
    "cancel_meeting": cancel_meeting,
    "list_upcoming_meeting": list_upcoming_meeting,
}

def api_call(chat_history):
        response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history,
        functions=functions,
        function_call="auto"
        )
        return response

def api_call_function(message,chat_history):
        func_name = message.function_call.name
        args = json.loads(message.function_call.arguments)
           
         # Dynamically call the function
        if func_name in function_map:
            result = function_map[func_name](**args)
        else:
            raise ValueError(f"Unknown function: {func_name}")

        # Append function response to memory
        chat_history.append({
                "role": "function",
                "name": func_name,
                "content": json.dumps(result)
        })

            # 🧠 Step 2: Call GPT again with tool output
        second_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_history
        )
        final_reply = second_response.choices[0].message.content
        return final_reply  


