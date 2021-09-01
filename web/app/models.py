import datetime

from django.db import models


class SensorReading(models.Model):
    name = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    stype = models.CharField(max_length=64)
    updated = models.DateTimeField('Time Last Updated')

    class Meta:
        unique_together = (('name', 'updated'))

    @staticmethod
    def save_model(obj):
        obj.updated = datetime.datetime.now(datetime.timezone.utc)
        obj.save()


class InfoMessage(models.Model):
    message = models.CharField(max_length=1024)
    level = models.IntegerField()
    updated = models.DateTimeField('Time Last Updated')

    @staticmethod
    def save_model(obj):
        obj.updated = datetime.datetime.now(datetime.timezone.utc)
        obj.save()


class VideoUrl(models.Model):
    url = models.CharField(max_length=256)
