from django.shortcuts import render
from django.http import JsonResponse
from services.mock_availability import get_free_busy_data
from candidate_fyi_takehome_project.interviews.helpers import get_all_available_time_blocks
from candidate_fyi_takehome_project.interviews.models import InterviewTemplate
# Create your views here.

def interviews_availability(request, id):
    interview = InterviewTemplate.objects.get(id=id)
    interviewer_query = interview.interviewer.values()
    interviewers = list(interviewer_query)
    interviewer_ids = list(interviewer_query.values_list('id', flat=True))
    duration = int(interview.duration)
    busy_data = get_free_busy_data(interviewers)
    json_resp = {
        "interviewId": id,
        "name": str(interview.name),
        "durationMinutes": duration,
        "interviewers": interviewers,
        "availableSlots": get_all_available_time_blocks(interviewer_ids, duration)
    }
    return JsonResponse(json_resp, safe=False)
