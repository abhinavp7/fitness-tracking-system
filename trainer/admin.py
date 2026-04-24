# from django.contrib import admin
# from .models import TrainerRequest, TrainerClient
# from fitness.models import Workout

# admin.site.register(TrainerRequest)
# admin.site.register(TrainerClient)
# admin.site.register(Workout)

from django.contrib import admin
from fitness.models import Workout

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'client', 'trainer', 'sets', 'reps', 'weight', 'date', 'status')
    list_filter = ('trainer', 'client', 'date')
    search_fields = ('exercise', 'client__username', 'trainer__username')
    readonly_fields = ('date',)

    def status(self, obj):
        return "Completed" if obj.completed else "Pending"

admin.site.register(Workout, WorkoutAdmin)
