from django.urls import path, include 
import first_app 

from .views import hello


urlpatterns = [
   # path('admin/', admin.site.urls),
    path('hello/', hello),
    path('hello/', hello),
]