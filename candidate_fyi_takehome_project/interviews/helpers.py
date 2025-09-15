from datetime import datetime, timedelta, UTC, time
from services.mock_availability import get_free_busy_data

def set_time_to_nearest_half_hour(dt_time: time) -> time:
    """
    Rounds up datetime time to nearest half hour.
    :param dt_time: datetime time to replace
    :returns: datetime time set to the nearest half hour
    """
    hour = dt_time.hour
    minute = dt_time.minute
    ms = dt_time.microsecond
    if ms > 0:
        minute += 1
    if 0 < minute <= 30:
        minute = 30
    elif 30 < minute <= 60:
        minute = 0
        hour += 1
    return time(hour=hour, minute=minute, second=0)


def get_all_possible_time_blocks(duration: int) -> list[dict[str, datetime]]:
    """
    Gets all possible time blocks for a given interview duration for the next week excluding Saturdays and Sundays.
    :param duration: duration in minutes of interview
    :returns: blocks of available times for the interview [{'start': start_datetime, 'end': end_datetime}, ...]
    Requirements:
        Slots must be exactly the duration minutes of the template
        Slots must begin on hour or half-hour marks (e.g., 10:00, 10:30)
        No slot may begin less than 24 hours in the future
        All times must be in UTC in ISO 8601 format
        Must exclude Saturday and Sunday.
        Must start and end between 9AM-5PM (9-17) UTC based on mock_availability
        Must match date range of 7 days based on mock_availability
    """
    start_datetime = datetime.now(UTC) + timedelta(days=1)
    start_date = start_datetime.date()
    start_time = set_time_to_nearest_half_hour(start_datetime.time())
    min_datetime = max(datetime.combine(start_date, start_time, tzinfo=UTC), datetime.combine(start_date, time(9), tzinfo=UTC))
    max_datetime = datetime.combine(start_date, time(17), tzinfo=UTC)
    time_blocks = []
    for day in range(6):
        if start_date.weekday() < 5:
            while min_datetime < max_datetime:
                end = min_datetime + timedelta(minutes=duration)
                if end <= max_datetime:
                    time_blocks.append({'start': min_datetime, 'end': end})
                min_datetime += timedelta(minutes=30)
        start_date += timedelta(days=1)
        min_datetime = datetime.combine(start_date, time(9), tzinfo=UTC)
        max_datetime += timedelta(days=1)
    return time_blocks

def get_time_blocks_from_busy_data(interviewers: list[int]) -> list[dict[str, datetime]]:
    """
    Gets all unavailable time blocks for the given interviewers.
    :param interviewers: list of interviewer ids
    :returns: blocks of unavailable times for the interview [{'start': start_datetime, 'end': end_datetime}, ...]
    """
    busy_data = get_free_busy_data(interviewers)
    unavailable_timeblocks = []
    for data in busy_data:
        slots = []
        for slot in data.get('busy', []):
            slots.append({'start': datetime.fromisoformat(slot['start']), 'end': datetime.fromisoformat(slot['end'])})
        unavailable_timeblocks.append(sorted(slots, key=lambda x: (x['start'], x['end'])))
    return unavailable_timeblocks


def get_all_available_time_blocks(interviewers: list[int], duration: int) -> list[dict[str, datetime]]:
    """
    Gets all possible time blocks for a given interview duration for the next week for the given interviewers.
    :param interviewers: list of interviewer ids
    :param duration: duration in minutes of interview
    Requirements:
        All interviewers must be available for the full slot duration
        All times must be in UTC in ISO 8601 format
    """
    unavailable_time_blocks = get_time_blocks_from_busy_data(interviewers)
    all_possible_time_blocks = get_all_possible_time_blocks(duration)
    for unavailable_timeblock in unavailable_time_blocks:
        possible_index = 0
        possible_length = len(all_possible_time_blocks)
        unavailable_index = 0
        unavailable_length = len(unavailable_timeblock)
        available_time_blocks = []
        while possible_index < possible_length:
            if unavailable_index >= unavailable_length:
                available_time_blocks.append(all_possible_time_blocks[possible_index])
                possible_index += 1
            elif all_possible_time_blocks[possible_index]['end'] <= unavailable_timeblock[unavailable_index]['start']:
                available_time_blocks.append(all_possible_time_blocks[possible_index])
                possible_index += 1
            elif all_possible_time_blocks[possible_index]['start'] >= unavailable_timeblock[unavailable_index]['end']:
                unavailable_index += 1
            else:
                possible_index += 1
        all_possible_time_blocks = available_time_blocks
    return all_possible_time_blocks
