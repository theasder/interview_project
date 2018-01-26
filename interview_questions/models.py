# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from interview_project import settings
import secretballot

class Votes(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    obj = models.TextField(max_length=20)
    obj_id = models.IntegerField()

class Topic(models.Model):
    name = models.CharField(max_length=80)
    screenname = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Problem(models.Model):
    POSITIONS = [('Стажёр', 'Стажёр'),
                 ('Junior', 'Junior'),
                 ('Middle', 'Middle'),
                 ('Senior', 'Senior'),
                 ('Teamlead', 'Teamlead')]
    TOPICS = [(elem['screenname'], elem['name']) for elem in Topic.objects.values('name', 'screenname')]

    title = models.CharField(max_length=80)
    problem_text = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(default=timezone.now)
    wiki_answer = models.TextField(max_length=5000, null=False, default='', blank=True)
    topic = models.CharField(max_length=50, blank=False, choices=TOPICS)
    position = models.CharField(max_length=50, null=True, blank=False, choices=POSITIONS)
    user = models.ForeignKey(User, null=True, blank=False, unique=False)
    vote = models.ForeignKey(Votes, null=True)
    total_votes = models.IntegerField(default=0)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def was_published_day(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def was_published_week(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now

    def was_published_month(self):
        now = timezone.now()
        return now - datetime.timedelta(days=30) <= self.pub_date <= now

# secretballot.enable_voting_on(Problem)

class Comment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True, blank=True)
    vote = models.ForeignKey(Votes, null=True)
    total_votes = models.IntegerField(default=0)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text

# secretballot.enable_voting_on(Comment)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True, blank=True)
    vote = models.ForeignKey(Votes, null=True)
    total_votes = models.IntegerField(default=0)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text

# secretballot.enable_voting_on(Reply)