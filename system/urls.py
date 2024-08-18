from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "system"


urlpatterns = [

    path('', views.LoginView, name = "login"), 
    path('sign-up', views.signUpView, name = "signup"), 
    path('dashboard', views.Dashboard, name = "dashboard"),
    path('chatbot/<int:id>', views.chatbotView, name='chatbot'),
    path('train/<int:id>', views.train, name = "train"),
    path('get_answer/', views.get_answerView, name='get_answer'),
    path('logout', views.logoutView, name = "logout"),

]+static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
