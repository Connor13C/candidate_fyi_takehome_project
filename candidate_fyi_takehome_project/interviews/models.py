from django.db import models
from faker import Faker

fake = Faker()


class Interviewer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default=fake.name())


class InterviewTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    interviewer = models.ManyToManyField('Interviewer')
