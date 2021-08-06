from django.urls import path,re_path
from .views import detectView



app_name='detect'
urlpatterns = [
    re_path(r'^detect/$', detectView, name='user_signup' ),
      
]
