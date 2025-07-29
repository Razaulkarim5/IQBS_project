from .import views
from django.urls import path 

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path("signout/", views.signout, name="signout"),
    path('home', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('view/', views.view, name='view'),
    path('analyze/', views.analyze, name='analyze'),
 #path('', views.data,name='data'),
     
]
