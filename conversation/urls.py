from django.urls import path
from .views import *


urlpatterns = [
    path('newconversation/<int:item_pk>/', newConversation, name='newconversation'),
    path('',inbox,name='inbox'),
    path('<int:pk>/', detail,name="detailll")
    ]