from django.db import models
from django.contrib.auth.models import User


class TrainerRequest(models.Model):
    trainer=models.ForeignKey(User,on_delete=models.CASCADE, related_name="received_request")
    client=models.ForeignKey(User,on_delete=models.CASCADE, related_name="sent_request")
    status=models.CharField(max_length=100,default="pending")
    
    def __str__(self):
        return f"{self.client}{self.trainer}({self.status})"
    
class TrainerClient(models.Model):
    trainer=models.ForeignKey(User, on_delete=models.CASCADE,related_name="trainer_client")
    client=models.ForeignKey(User,on_delete=models.CASCADE,related_name="client_trainer")
    
    def __str__(self):
        return f"{self.trainer.username}-{self.client.username}"
    

class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="receive_messages")
    text=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    
    