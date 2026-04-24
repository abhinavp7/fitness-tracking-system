"""
URL configuration for fitness_tracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fitness import views
from trainer import views as trainer_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workout',views.WorkoutView.as_view(), name="workout"),
    path('', views.UserLoginView.as_view(), name="login"),
    path('register',views.UserRegisterView.as_view(), name="user_register"),
    path('logout', views.Logoutview.as_view(), name="logout"),
    path('delete/<int:id>',views.WorkoutDeleteView.as_view(),name="delete_workout"),
    path('update/<int:id>',views.UpdateWorkoutView.as_view(), name="update_workout"),
    path('workout/<int:id>/demo/', views.WorkoutDemoView.as_view(), name='workout_demo'),
    path('trainers',trainer_view.TrainerListView.as_view(), name="trainer_list"),
    path('send/<int:id>',trainer_view.SendRequestView.as_view(), name="send_request"),
    path('trainer/dashboard',trainer_view.TrainerDashBoardView.as_view(),name="trainer_dashboard"),
    path('request/accept/<int:id>', trainer_view.AcceptRequestView.as_view(), name="accept_request"),
    path('request/reject/<int:id>', trainer_view.RejectRequestView.as_view(), name="reject_request"),
    path('client/<int:id>',trainer_view.ClientDetailView.as_view(),name="client_detail"),
    path('trainer/delete-workout/<int:id>',trainer_view.TrainerDeleteWorkoutView.as_view(),name="delete_workout_trainer"),
    path('trainer/update-workout/<int:id>',trainer_view.TrainerUpdateWorkoutView.as_view(),name="update_workout_trainer"),
    path('chat/<int:id>',trainer_view.ChatView.as_view(),name="chat"),
    path('my-workouts/',trainer_view.ClientWorkoutView.as_view(),name='client_workouts'),
    path('complete/<int:id>/',trainer_view.CompleteWorkoutView.as_view(),name='complete_workout'),
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

