from django.db import models
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import json


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Model):
            return model_to_dict(obj)
        return super().default(obj)

class Interviewer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class InterviewTemplate(models.Model):
    interviewId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    durationMinutes = models.IntegerField()
    interviewers = models.ManyToManyField('Interviewer')

    @classmethod
    def get_json_by_id(cls, _id:int) -> dict:
        """
        Gets the json representation of the interview
        :param _id: interviewId of InterviewTemplate
        :returns: json object of InterviewTemplate
        """
        interview = InterviewTemplate.objects.get(interviewId=_id)
        return json.loads(json.dumps(interview, cls=ExtendedEncoder))
