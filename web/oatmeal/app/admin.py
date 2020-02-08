from django.contrib import admin

from .models import SensorReading
from .models import InfoMessage
from .models import VideoUrl

admin.site.register(SensorReading)
admin.site.register(InfoMessage)
admin.site.register(VideoUrl)
