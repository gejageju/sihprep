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
    path('applications',views.applicationList.as_view()),
    path('printdata',views.printdata.as_view()),
    path('onetap',views.onetapsignin.as_view()),
    path('addToFav',views.addToFav.as_view()),
    path('removeFromFav',views.removeFromFav.as_view()),
    path('getFav',views.getFavs.as_view()),
    path('getquesbysubj',views.getQuesBySubj.as_view()),
    path('quesByMe',views.getQuesByMe.as_view()),
    path('checkemail',views.checkemail.as_view()),
    path('',views.index)
]