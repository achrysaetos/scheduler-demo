from datetime import datetime, timedelta
from typing import List, Dict

PREFERRED_GRANULARITY = 15  # how much time results can overlap, in case people like having a tight schedule
TARGET_TIME = 13 * 60  # determine when the best meeting times should be - default is middle of the workday (1:00 PM) in minutes
NUM_RESULTS = 5  # upper bound on the number of results to return

def findAvailableSlots(schedules: List[List[Dict[str, str]]], duration: int) -> List[Dict[str, str]]:
    # Convert all scheduled times to a range of unavailable minutes
    busy_minutes = []
    for schedule in schedules:
        busy_minutes.extend([
            (iso_to_minutes(slot['start']), iso_to_minutes(slot['end']))
            for slot in schedule
        ])

    # Sort busy times and merge overlapping intervals
    busy_minutes.sort(key=lambda x: x[0])
    merged_busy = []
    for start, end in busy_minutes:
        if not merged_busy or start > merged_busy[-1][1]:
            merged_busy.append([start, end])
        else:
            merged_busy[-1][1] = max(merged_busy[-1][1], end)

    # Find intervals when everyone is free
    free_slots = []
    day_start = 0
    day_end = 24 * 60

    for i, (busy_start, busy_end) in enumerate(merged_busy):
        if i == 0 and busy_start - day_start >= duration:
            free_slots.append({'start': day_start, 'end': busy_start})
        if i > 0:
            prev_end = merged_busy[i-1][1]
            if busy_start - prev_end >= duration:
                free_slots.append({'start': prev_end, 'end': busy_start})
        if i == len(merged_busy) - 1 and day_end - busy_end >= duration:
            free_slots.append({'start': busy_end, 'end': day_end})

    # From the calculated free times, generate all possible slots of length 'duration'
    all_slots = []
    for slot in free_slots:
        start = slot['start']
        while start + duration <= slot['end']:
            all_slots.append({'start': start, 'end': start + duration})
            start += PREFERRED_GRANULARITY # Move start time by the target interval
    
    # Sort slots based on proximity to the preferred target time
    sorted_slots = sorted(all_slots, key=lambda slot: abs(((slot['start'] + slot['end']) / 2) - TARGET_TIME))

    # Select top 5 options
    best_slots = sorted_slots[:NUM_RESULTS]

    # Convert to ISO format
    base_date = schedules[0][0]['start'].split('T')[0]
    iso_slots = [
        {
            'start': minutes_to_iso(slot['start'], base_date + 'T00:00:00Z'),
            'end': minutes_to_iso(slot['end'], base_date + 'T00:00:00Z')
        }
        for slot in best_slots
    ]

    return iso_slots


def iso_to_minutes(iso_time: str) -> int:
    """Convert ISO format time to minutes since start of the day."""
    dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
    return dt.hour * 60 + dt.minute


def minutes_to_iso(minutes: int, base_date: str) -> str:
    """Convert minutes since start of the day to ISO format time."""
    base_dt = datetime.fromisoformat(base_date.replace('Z', '+00:00'))
    new_dt = (base_dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes=minutes))
    return new_dt.isoformat().replace('+00:00', 'Z')


"""
Example usage (test inputs here):
"""
schedules = [
    [{'start': "2023-10-17T09:00:00Z", 'end': "2023-10-17T10:30:00Z"}, {'start': "2023-10-17T12:00:00Z", 'end': "2023-10-17T13:00:00Z"}, {'start': "2023-10-17T16:00:00Z", 'end': "2023-10-17T18:00:00Z"}],
    [{'start': "2023-10-17T10:00:00Z", 'end': "2023-10-17T11:30:00Z"}, {'start': "2023-10-17T12:30:00Z", 'end': "2023-10-17T14:30:00Z"}, {'start': "2023-10-17T14:30:00Z", 'end': "2023-10-17T15:00:00Z"}, {'start': "2023-10-17T16:00:00Z", 'end': "2023-10-17T17:00:00Z"}],
    [{'start': "2023-10-17T11:00:00Z", 'end': "2023-10-17T11:30:00Z"}, {'start': "2023-10-17T12:00:00Z", 'end': "2023-10-17T13:30:00Z"}, {'start': "2023-10-17T14:00:00Z", 'end': "2023-10-17T16:30:00Z"}]
]
duration = 30
result = findAvailableSlots(schedules, duration)
print("Available slots:", result)
