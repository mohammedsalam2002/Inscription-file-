from django.urls import path ,include
from .views import *

urlpatterns = [
    path('', user_login, name='login'),  # Custom login view
    path('signup/', signup, name='signup'),
    path('logout/', logout_1, name='logout'),
    path('home/', home,name='home'),
    path('encrypt/', encrypt,name='encrypt'),
    path('decrypt/', decrypt,name='decrypt'),
    
    
]