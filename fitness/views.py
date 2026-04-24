from django.shortcuts import render,redirect
from fitness.models import Workout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from fitness.forms import UserRegisterForm,UserLoginForm
from trainer.models import TrainerClient
from django.shortcuts import get_object_or_404

class UserRegisterView(View):
    def get(self,request):
        form = UserRegisterForm()
        return render(request,'user_register.html',{'form':form})
    
    
    def post(self,request):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            User.objects.create_user(username=username,email=email,password=password)
            messages.success(request,"Account Created Successfully")
            return redirect("login")

        else:
            print(form.errors)
            return render(request,'user_register.html',{'form':form})
        



class UserLoginView(View):
    def get(self,request):
        form=UserLoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request):
        uname=request.POST.get("username")
        psw=request.POST.get("password")
        res=authenticate(request,username=uname,password=psw)
        if res:
            login(request, res)

            if res.is_staff:  
                return redirect("trainer_dashboard")
            else:             
                return redirect("workout")
        else:
            messages.warning(request, "invalid credentials")
            return redirect("login")
        
        
        
class Logoutview(View):
    def get(self,request):
        logout(request)
        messages.success(request,'logout successful')
        return redirect("login")


class WorkoutView(LoginRequiredMixin,View):
    def get(self,request):
        workout=Workout.objects.filter(client=request.user)
        trainer=TrainerClient.objects.filter(client=request.user).first()
        return render(request,"workout.html",{"workout":workout,"trainer":trainer})
    def post(self, request):
        exercise = request.POST.get("exercise")
        sets = int(request.POST.get("sets"))
        reps = int(request.POST.get("reps"))
        weight = float(request.POST.get("weight"))

        trainer_obj = TrainerClient.objects.filter(client=request.user).first()

        if not trainer_obj:
            messages.warning(request, "You need a trainer before adding workouts.")
            return redirect("workout")

        Workout.objects.create(
            trainer=trainer_obj.trainer,
            client=request.user,
            exercise=exercise,
            sets=sets,
            reps=reps,
            weight=weight
        )

        return redirect("workout")
            
class WorkoutDeleteView(View):
    def get(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"),client=request.user)
        workout.delete()
        return redirect("workout")
    
    
class UpdateWorkoutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"),client=request.user)
        return render(request,"edit_workout.html",{"workout":workout})
    
    def post(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"),client=request.user)
        workout.exercise=request.POST.get("exercise")
        workout.sets=request.POST.get("sets")
        workout.reps=request.POST.get("reps")
        workout.weight=request.POST.get("weight")
        workout.save()
        return redirect("workout")
    
    
from django.shortcuts import render,redirect
from fitness.models import Workout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from fitness.forms import UserRegisterForm,UserLoginForm
from trainer.models import TrainerClient
from django.shortcuts import get_object_or_404

class UserRegisterView(View):
    def get(self,request):
        form = UserRegisterForm()
        return render(request,'user_register.html',{'form':form})
    
    
    def post(self,request):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            User.objects.create_user(username=username,email=email,password=password)
            messages.success(request,"Account Created Successfully")
            return redirect("login")

        else:
            print(form.errors)
            return render(request,'user_register.html',{'form':form})
        



class UserLoginView(View):
    def get(self,request):
        form=UserLoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request):
        uname=request.POST.get("username")
        psw=request.POST.get("password")
        res=authenticate(request,username=uname,password=psw)
        if res:
            login(request, res)

            if res.is_staff:  
                return redirect("trainer_dashboard")
            else:             
                return redirect("workout")
        else:
            messages.warning(request, "invalid credentials")
            return redirect("login")
        
        
        
class Logoutview(View):
    def get(self,request):
        logout(request)
        messages.success(request,'logout successful')
        return redirect("login")


class WorkoutView(LoginRequiredMixin,View):
    def get(self,request):
        workout=Workout.objects.filter(client=request.user)
        trainer=TrainerClient.objects.filter(client=request.user).first()
        return render(request,"workout.html",{"workout":workout,"trainer":trainer})
    def post(self, request):
        exercise = request.POST.get("exercise")
        sets = int(request.POST.get("sets"))
        reps = int(request.POST.get("reps"))
        weight = float(request.POST.get("weight"))
        video = request.POST.get("video") 
        trainer_obj = TrainerClient.objects.filter(client=request.user).first()

        if not trainer_obj:
            messages.warning(request, "You need a trainer before adding workouts.")
            return redirect("workout")

        Workout.objects.create(
            trainer=trainer_obj.trainer,
            client=request.user,
            exercise=exercise,
            sets=sets,
            reps=reps,
            weight=weight,
            video=video 
        )

        return redirect("workout")
            
class WorkoutDeleteView(View):
    def get(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"),client=request.user)
        workout.delete()
        return redirect("workout")
    
    
class UpdateWorkoutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"),client=request.user)
        return render(request,"edit_workout.html",{"workout":workout})
    
    def post(self,request,*args,**kwargs):
        workout=Workout.objects.get(id=kwargs.get("id"),client=request.user)
        workout.exercise=request.POST.get("exercise")
        workout.sets=request.POST.get("sets")
        workout.reps=request.POST.get("reps")
        workout.weight=request.POST.get("weight")
        workout.save()
        print("POST DATA:", request.POST)
        print("VIDEO:", request.POST.get("video"))
        return redirect("workout")
    
    
class WorkoutDemoView(View):
    def get(self,request,id):
        workout=get_object_or_404(Workout,id=id)
        return render(request,'workout_demo.html',{'workout':workout})