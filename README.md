# 🧠 Backend Take-Home: **Dynamic Interview Slot Generator (Django)**

---

## 🚀 Setup instructions

### Using Docker

This project includes Docker configuration for easy setup and consistent environments.

1. **Make sure Docker and Docker Compose are installed on your system**

2. **Build and start the application**
   ```bash
   # Build and start all services
   make up
   
   # Or alternatively
   docker compose -f docker-compose.local.yml up --remove-orphans -d
   ```

3. **Run migrations**
   ```bash
   make makemigrations
   
   # Or alternatively
   docker exec candidate_fyi_takehome_project_local_django python manage.py makemigrations
   ```
   
4. **Run migrations**
   ```bash
   make migrate
   
   # Or alternatively
   docker exec candidate_fyi_takehome_project_local_django python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   make superuser
   
   # Or alternatively
   docker exec -it candidate_fyi_takehome_project_local_django bash
   python manage.py superuser
   ```

6. **Access the API**
   
   The API will be available at: http://localhost:8000/api/interviews/<id>/availability

### Other Useful Commands

```bash
# Stop all containers
make down

# Or alternatively
docker compose -f docker-compose.local.yml down
```

---

## 📦 Design decisions
- Interviews should only be available for weekdays so on Saturday and Sunday interviewers were considered to be busy the entire day
- Interviews must start and end between 9AM-5PM (9-17) UTC based on mock_availability
- Interviews must match date range of 7 days based on mock_availability
- Interviewer names stored in Interviewer database table while utilizing Faker instead of mock_availability due to it being more standard and coherent


---

## Edge case write-up

- What the case was:
  - In mock_availability the random generator of busy time blocks could potentially produce two overlapping time blocks,
  like 1PM-2PM and 1PM-3PM on the same day for a given interviewer which could be accidently sorted like [1PM-3PM, 1PM-2PM].
- Why it mattered
  - My solution to building a list of available times was to first build all list of all times that a interview could take place, then take the list of unavailable times from mock_availability and remove them. The conditions I was checking for while iterating through both arrays was if the end time of possible time block was less than or equal to the start time of the unavailable time block then I knew that I could add it to available time blocks and the second condition was the start time of the possible time block was greater than or equal to the end time of the available block then I would need to check the next blocked time. Since the unavailable time blocks could be sorted by start time but not end time it could allow some time blocks to be kept in that were not actually available.
- How you handled it
  - Once I determined through testing that this problem could occur I then chose to sort on two criteria instead of one with my primary on start time and my secondary on end time.
---

# Initial Specifications
## 🗂️ Overview

In this take-home challenge, you'll implement a backend feature for a scheduling tool like [candidate.fyi](https://candidate.fyi/). The goal is to **dynamically generate potential interview time slots** by intersecting the real-time availability of multiple interviewers.

Unlike systems with static slots, this exercise simulates a more realistic setup — pulling external calendar data, evaluating overlapping availability, and applying constraints.

---

## 🎯 Goal

Build an API that, given an interview template ID, returns potential time slots where **all assigned interviewers are available at the same time** for the required duration.

---

## 🛠️ Tech Stack

You must use:

- Python 3.10+
- Django 4.x
- Django REST Framework (DRF)
- SQLite or PostgreSQL
- Faker (already used in provided helper)

---

## 📋 Core Requirements

### ✅ Models

You'll need to implement models to support this feature. At a minimum:

- `Interviewer`: represents someone who conducts interviews
- `InterviewTemplate`: represents a type of interview, with:
    - A name (e.g., "Technical Interview")
    - A duration in minutes (e.g., 60)
    - A many-to-many relationship to Interviewers

You're free to design additional models if it helps with clarity or flexibility.

---

### ✅ Endpoint

```bash
GET /api/interviews/<id>/availability
```

This endpoint should:

1. Load the `InterviewTemplate` with the given ID
2. Use the **provided mock service** to fetch availability for all associated interviewers
3. Return **only time slots where all interviewers are simultaneously available** for the required duration
4. Format the result as a JSON response

---

## 🧾 Interviewer Availability Service

To simulate the external calendar system, use the helper in:

```
service/mock_availability.py
```

Import and call the function like so:

```python
from service.mock_availability import get_free_busy_data

interviewer_ids = [1, 2]
busy_data = get_free_busy_data(interviewer_ids)

```

### 🔄 Sample Output

```json
[
  {
    "interviewerId": 1,
    "name": "Alice Johnson",
    "busy": [
      { "start": "2025-01-22T09:00:00Z", "end": "2025-01-22T12:00:00Z" }
    ]
  },
  {
    "interviewerId": 2,
    "name": "Bob Smith",
    "busy": [
      { "start": "2025-01-22T10:00:00Z", "end": "2025-01-22T13:00:00Z" }
    ]
  }
]
```

> ✅ You are welcome to enhance or modify this service as needed — e.g., to support filtering, partial day simulation, or sorting.

---

## 📤 API Response Format

```json
{
  "interviewId": 1,
  "name": "Technical Interview",
  "durationMinutes": 60,
  "interviewers": [
    { "id": 1, "name": "Alice Johnson" },
    { "id": 2, "name": "Bob Smith" }
  ],
  "availableSlots": [
    {
      "start": "2025-01-22T10:00:00Z",
      "end": "2025-01-22T11:00:00Z"
    },
    {
      "start": "2025-01-22T11:00:00Z",
      "end": "2025-01-22T12:00:00Z"
    }
  ]
}
```

---

## ⚠️ Constraints

You must enforce the following:

- Slots must be **exactly** the duration minutes of the template
- Slots must begin on **hour or half-hour marks** (e.g., 10:00, 10:30)
- **All interviewers must be available** for the full slot duration
- **No slot may begin less than 24 hours** in the future
- All times must be in **UTC** in ISO 8601 format

---

### 🧠 Developer Insight (Required)

In addition to meeting the requirements above, we'd like you to demonstrate how you think beyond the surface.

### ✅ What to Do:

As part of your submission, please identify **one unique edge case or complexity** you encountered that wasn't explicitly mentioned in the prompt.

- This could relate to availability overlaps, data inconsistencies, ambiguous logic, or system design.
- Implement your handling of it in the code.
- Add a short explanation in your README:
    - What the case was
    - Why it mattered
    - How you handled it

### 💡 Why:

In real-world systems, requirements evolve and edge cases emerge. We want to see how you anticipate and reason about those situations — not just follow a spec.

---

## 📦 Submission

Submit a GitHub repo with:

- All source code
- Your own models, views, serializers
- README with:
    - Setup instructions
    - Design decisions
    - Your extra edge case write-up


