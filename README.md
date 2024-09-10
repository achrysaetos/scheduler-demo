# Scheduler Demo

This algorithm takes 1) a list of busy schedules and 2) a meeting duration, and returns a list of the 5 best meeting times for all people.

Unless specified, the algorithm will prefer times that are neither too early nor too late, and will default to an offering of times that is 15 minutes apart (in case people like having a tight schedule).

## Usage

```
python scheduler.py
```
Runs the `findAvailableSlots` function with custom test input. (Python 3.9+ recommended)

## How it works

1. Combine all the busy times into a range of unavailable minutes. For simplicity, this is represented as a list of tuples in minutes since midnight.
2. Merge the overlapping busy minutes and calculate the intervals when everyone is free.
3. From these free intervals, generate a list of all possible meeting times with the required duration. The gap between intervals can overlap by a default of 15 minutes (so people can start meetings at 4:15 for example).
4. Select the 5 best preferred times and convert them back to ISO format. In this case, the best times are the ones that are closest to the middle of the workday.

## Example
```
const schedules = [
    [{start: "2023-10-17T09:00:00Z", end: "2023-10-17T10:30:00Z"}, {start: "2023-10-17T12:00:00Z", end: "2023-10-17T13:00:00Z"}, {start: "2023-10-17T16:00:00Z", end: "2023-10-17T18:00:00Z"}],
    [{start: "2023-10-17T10:00:00Z", end: "2023-10-17T11:30:00Z"}, {start: "2023-10-17T12:30:00Z", end: "2023-10-17T14:30:00Z"}, {start: "2023-10-17T14:30:00Z", end: "2023-10-17T15:00:00Z"}, {start: "2023-10-17T16:00:00Z", end: "2023-10-17T17:00:00Z"}],
    [{start: "2023-10-17T11:00:00Z", end: "2023-10-17T11:30:00Z"}, {start: "2023-10-17T12:00:00Z", end: "2023-10-17T13:30:00Z"}, {start: "2023-10-17T14:00:00Z", end: "2023-10-17T16:30:00Z"}]
];
const duration = 30;

# Unavailable minutes (when not everyone can make it)
[(540, 630), (720, 780), (960, 1080), (600, 690), (750, 870), (870, 900), (960, 1020), (660, 690), (720, 810), (840, 990)]

# Merged unavailable minutes
[[540, 690], [720, 1080]]

# Free intervals (when everyone can make it)
[{'start': 0, 'end': 540}, {'start': 690, 'end': 720}, {'start': 1080, 'end': 1440}]

# All possible slots of length 30 minutes, with a custom granularity of 15 minutes
[{'start': 0, 'end': 30}, {'start': 15, 'end': 45}, {'start': 30, 'end': 60}, ..., {'start': 1380, 'end': 1410}, {'start': 1395, 'end': 1425}, {'start': 1410, 'end': 1440}]

# Best slots (closest to the middle of the workday - 1:00 PM, or 780 minutes past midnight)
[{'start': 690, 'end': 720}, {'start': 510, 'end': 540}, {'start': 495, 'end': 525}, {'start': 480, 'end': 510}, {'start': 465, 'end': 495}]

# Best slots converted back to ISO format
[{'start': '2023-10-17T11:30:00Z', 'end': '2023-10-17T12:00:00Z'}, {'start': '2023-10-17T08:30:00Z', 'end': '2023-10-17T09:00:00Z'}, {'start': '2023-10-17T08:15:00Z', 'end': '2023-10-17T08:45:00Z'}, {'start': '2023-10-17T08:00:00Z', 'end': '2023-10-17T08:30:00Z'}, {'start': '2023-10-17T07:45:00Z', 'end': '2023-10-17T08:15:00Z'}]
```

## Runtime

The runtime of this algorithm is O(n log n), where n is the number blocks of time of length `duration` in a day. This is because it's dominated by the sorting step - everything else is linear, such as merging overlapping intervals and finding free slots.
