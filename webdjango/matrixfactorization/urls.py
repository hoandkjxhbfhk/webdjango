from django.urls import path

from . import views
app_name = 'matrixfactorization'
urlpatterns = [
    path('recommend/',views.recomend,name='recommend')
]