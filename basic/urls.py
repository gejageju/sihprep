from django.contrib import admin
from django.urls import path,include
from . import views
from .views import index
urlpatterns = [
    path('addQuestion',views.CreateQuestionview.as_view()),
    path('recent', views.FetchRecentQuestions.as_view()),
    path('verifyQuestion',views.VerifyQuestion.as_view()),
    path('rejectQuestion',views.RejectQuestion.as_view()),
    path('getNotifications',views.getNotifications.as_view()),
    #path('createUser',views.CreateUser.as_view()),
    path('printdata',views.printdata.as_view()),
    path('',views.index)
]