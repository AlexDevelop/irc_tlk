from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TodoType(TimeStampedModel):
    group = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.group


class TodoList(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False)
    todo_type = models.ForeignKey(to=TodoType)
    description = models.CharField(max_length=1024, blank=False)
    data = models.TextField(blank=False)
    date_deadline = models.DateTimeField()
    identifier = models.IntegerField(blank=True)
    status = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

class Setting(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False)
    channel = models.CharField(max_length=255, blank=False)
    value = models.CharField(max_length=255, blank=False)
    setting_data = models.ForeignKey(to='SettingData')

    def __str__(self):
        #name = 'TestName'
        #channel = 'TestChannel'

        #if self.name:
       #:x     name = self.name

        #if self.channel:
        #    channel = self.channel
        #return "{name} - {channel}".format(name=name, channel=channel)
        return self.name

class SettingData(TimeStampedModel):
    _key = models.CharField(max_length=255, blank=False)
    _value = models.CharField(max_length=255, blank=False)
