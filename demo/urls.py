from django.urls import path
from .views import *




urlpatterns = [
    path('parser', ParserDemo.as_view()),
    path('serializers', SerializersDemo.as_view()),
    path('serializers/userInfo', SerializersUserInfo.as_view()),
    path('page/roles', PageRoles.as_view()),
]
