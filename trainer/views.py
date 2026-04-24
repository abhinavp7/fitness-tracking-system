from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views import View
from trainer.models import TrainerRequest
from trainer.models import TrainerClient,Message
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from fitness.models import Workout


class TrainerListView(View):
    def get(self,request):
        trainers=User.objects.filter(is_staff=True)
        return render (request,"trainer_list.html",{"trainers":trainers})


class SendRequestView(View):
    def get(self,request,*args,**kwargs):
        trainer=User.objects.get(id=kwargs.get("id"))
        if not TrainerRequest.objects.filter(trainer=trainer,client=request.user).exists():
            TrainerRequest.objects.create(trainer=trainer,client=request.user)
            messages.success(request, "Request sent successfully!")
        else:
            messages.warning(request,"Request already sent")
        return redirect("trainer_list")
    
class TrainerDashBoardView(LoginRequiredMixin,View):
    def get(self,request):
        req=TrainerRequest.objects.filter(trainer=request.user,status="pending")
        client=TrainerClient.objects.filter(trainer=request.user)
        return render(request,"trainer_dashboard.html",{"req":req,"client":client})
        
    
class AcceptRequestView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        req=TrainerRequest.objects.get(id=kwargs.get("id"))
        req.status="accepted"
        req.save()
        TrainerClient.objects.create(trainer=request.user,client=req.client)
        return redirect("trainer_dashboard")
    
class RejectRequestView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        req=TrainerRequest.objects.get(id=kwargs.get("id"))
        req.status="Rejected"
        req.save()
        return redirect("trainer_dashboard")
    
class ClientDetailView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        assign=TrainerClient.objects.filter(trainer=request.user,client=user).exists()
        if not assign:
            return redirect("trainer_dashboard")
        workouts= Workout.objects.filter(client=user, trainer=request.user).order_by('-date')
        
        return render(request,"client_detail.html",{"client":user,"workouts":workouts})
    
    def post(self,request,*args,**kwargs):
        user=User.objects.get(id=kwargs.get("id"))
        assign=TrainerClient.objects.filter(trainer=request.user,client=user).exists()
        if not assign:
            return redirect("trainer_dashboard")
        Workout.objects.create(
            trainer=request.user,
            client=user,
            exercise=request.POST.get("exercise"),
            sets=int(request.POST.get("sets")),
            reps=int(request.POST.get("reps")),
            weight=float(request.POST.get("weight"))
        )

        return redirect("client_detail", id=user.id)
    

class TrainerDeleteWorkoutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"))
        assign = TrainerClient.objects.filter(trainer=request.user, client=workout.client).exists()
        if not assign:
            return redirect("trainer_dashboard")
        client_id = workout.client.id
        workout.delete()
        return redirect("client_detail", id=client_id)
    
class TrainerUpdateWorkoutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"))
        assign=TrainerClient.objects.filter(trainer=request.user,client=workout.client).exists()
        if not assign:
            return redirect("trainer_dashboard")
        return render(request,"trainer_edit_workout.html",{"workout":workout})
    
    def post(self, request, *args, **kwargs):
        workout = Workout.objects.get(id=kwargs.get("id"))

        assign = TrainerClient.objects.filter(
            trainer=request.user,
            client=workout.client
        ).exists()

        if not assign:
            return redirect("trainer_dashboard")

        workout.exercise = request.POST.get("exercise")
        workout.sets = int(request.POST.get("sets"))
        workout.reps = int(request.POST.get("reps"))
        workout.weight = float(request.POST.get("weight"))

        # 💥 FIX: use POST, NOT FILES
        video = request.POST.get("video")

        if video:
            workout.video = video

        workout.save()

        return redirect("client_detail", id=workout.client.id)
    
    
class ChatView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        other_user= User.objects.get(id=kwargs.get("id"))
        is_valid=TrainerClient.objects.filter(trainer=request.user,client=other_user).exists() or TrainerClient.objects.filter(trainer=other_user,client=request.user).exists()
        if not is_valid:
            if request.user.is_superuser:
                return redirect("trainer_dashboard")
            else:
                return redirect("workout")

        messages=Message.objects.filter(
            sender__in=[request.user,other_user],
            receiver__in=[request.user,other_user]
        ).order_by("timestamp")
        
        return render(request,"chat.html",{"messages":messages,"other_user":other_user})
    
    
    def post(self,request,*args,**kwargs):
        other_user=User.objects.get(id=kwargs.get("id"))
        text=request.POST.get("text")
        assign = TrainerClient.objects.filter(trainer=request.user,client=other_user).exists() or TrainerClient.objects.filter(trainer=other_user,client=request.user).exists()
        if not assign:
            if request.user.is_superuser:
                return redirect("trainer_dashboard")
            else:
                return redirect("workout")

        if text and text.strip():
            Message.objects.create(sender=request.user,receiver=other_user,text=text)

        return redirect("chat",id=other_user.id)
    

class ClientWorkoutView(LoginRequiredMixin,View):
    def get(self,request):
        workouts=Workout.objects.filter(client=request.user).order_by('-date')
        return render(request,"client_workouts.html",{"workouts":workouts})
    
class CompleteWorkoutView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"))
        if workout.client!=request.user:
            return redirect("workout")
        
        workout.completed=True
        workout.save()
        return redirect("client_workouts")
    