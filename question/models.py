from django.db import models
from account.models import Profile
from django.utils import timezone


class Topic(models.Model):
    image = models.FileField()
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Question(models.Model):
    profile = models.ForeignKey(Profile)
    content = models.CharField(max_length=200)
    picture = models.FileField(blank=True, default=None, null=True)
    topic = models.ForeignKey(Topic)
    views = models.IntegerField(default=0)
    q_like=models.IntegerField(default=0)
    q_dislike = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Answer(models.Model):
    profile = models.ForeignKey(Profile)
    content = models.CharField(max_length=3000)
    picture = models.FileField(blank=True, default=None, null=True)
    question = models.ForeignKey(Question)
    a_like = models.IntegerField(default=0)
    a_dislike = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Follow(models.Model):
    profile = models.ForeignKey(Profile)
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return self.profile.user.username + " follows " + self.topic.title

class Comment(models.Model):
    profile = models.ForeignKey(Profile)
    content = models.CharField(max_length=3000)
    picture = models.FileField(blank=True, default=None, null=True)
    answer = models.ForeignKey(Answer)
    c_like = models.IntegerField(default=0)
    c_dislike = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
