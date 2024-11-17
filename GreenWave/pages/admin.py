from django.contrib import admin
from .models import user_profile
from .models import campaign
from .models import service
from .models import Place
from .models import reward
# Register your models here.

admin.site.register(user_profile)
admin.site.register(campaign)
admin.site.register(service)
admin.site.register(Place)
admin.site.register(reward)
