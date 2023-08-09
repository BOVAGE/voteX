from django.contrib import admin
from .models import Voter


# Register your models here.
@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ["id", "election", "email", "is_verified"]
