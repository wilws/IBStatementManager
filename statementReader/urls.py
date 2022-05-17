from django.urls import path

from statementReader import views
urlpatterns = [
	path('',views.index),
]