from django.contrib import admin

# Register your models here.
from .models import Category, Event, Participant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'location', 'category')
    list_filter = ('category', 'date')
    search_fields = ('name', 'location')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
