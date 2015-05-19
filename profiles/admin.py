from django.contrib import admin

from reversion import VersionAdmin

from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(VersionAdmin):
    pass