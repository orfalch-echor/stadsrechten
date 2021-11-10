from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    subject = models.CharField(
        max_length=100,
        help_text=_("Enter a subject for the todo (max. 100 characters)")
    )
    description = models.TextField(
         help_text=_('Detailed desciption of the todo item.')
    )
    starttime = models.DateTimeField(
        auto_now=True,
        help_text=_('Starttime for todo')
    )
    endtime = models.DateTimeField(
        auto_now=True,
        help_text=_('Endtime for todo')
    )
    done = models.BooleanField(
        default=False,
        help_text=_('Todo item is done.'),
    )
    reminder = models.BooleanField(
        default=False,
        help_text=_('Send a reminder at the starttime'),
    )

    def __str__(self):
        return self.subject


class Selection(models.Model):
    selected = models.DateTimeField(
        null=True,
        default=datetime.now)
    todo = models.CharField(max_length=100, blank=True, null=True)


class History(models.Model):
    todo = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    rank = models.IntegerField()


class Timeblock(models.Model):
    name = models.CharField(max_length=50)
    start = models.TimeField(default='00:00:00')
    end = models.TimeField(default='23:59:59')
    todo = models.ManyToManyField(Todo)

    def __str__(self):
        return self.name
