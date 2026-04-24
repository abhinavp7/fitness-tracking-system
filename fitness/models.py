from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_workouts')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_workouts')
    exercise= models.CharField(max_length=100)
    sets=models.IntegerField()
    reps= models.IntegerField()
    weight=models.FloatField()
    completed = models.BooleanField(default=False)
    date=models.DateField(auto_now_add=True)
    
    video = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.client.username} - {self.exercise} ({self.sets}x{self.reps})"