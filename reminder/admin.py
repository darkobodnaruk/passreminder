from django.contrib import admin
from reminder.models import Account, PassHash

admin.site.register(Account)
admin.site.register(PassHash)