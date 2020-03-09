from django.urls import path
from . import views

urlpatterns = [
	path('',views.index, name='index'),
	path('do_login',views.authenticate, name='auth'),
	path('test',views.test, name='get')
]