from django.contrib import admin
from django.urls import path, include
from accountbook.views.views import Home, Register, Change, DataChange, Inquiry, Delete, CategoryRegister


app_name = 'accountbook'

urlpatterns = [
    path('register/', Register.create, name='register'),
    path('change/', Change.as_view(), name='change'),
    path('change/<int:pk>', DataChange.change, name='datachange'),
    path('update/', DataChange.change, name='datachange'),
    path('inquiry/', Inquiry.as_view(), name='Inquiry'),
    path('delete/<int:pk>', Delete.as_view(), name='delete'),
    path('register/category', CategoryRegister.create, name='register category')
]