from array import array
from urllib import response
from django.shortcuts import render
from .models import  Notifications, Question,applications,UserProfile
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.http import JsonResponse
from .serializers import QuestionSerializer,UserProfileSerializer,applicationSerializers
# Create your views here.

def index(request):
    return  render(request,'index.html')


class CreateQuestionview(APIView):
  
  def post(self,request):
    #temp=request.data
    print(request.data)
    serializer = QuestionSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""class CreateUserProfile(APIView):
    def post(self,request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""


class FetchRecentQuestions(generics.ListAPIView):

    queryset=Question.objects.all().filter(isVerified=True)
    queryset=queryset.order_by('-createdAt')[:10]
    serializer_class = QuestionSerializer

class VerifyQuestion(APIView):

    def post(self,request):
      id=request.data["questionId"]
      obj=Question.objects.get(id=id)
      obj.isVerified=True
      obj.verifiedBy = request.data["verifierId"]
      obj.save()
      userId= obj.uploadedBy
      notifobj= Notifications()
      notifobj.userId=userId
      notifobj.msg="Your question has been verified!"
      notifobj.save()
      return Response(status=status.HTTP_201_CREATED)

class RejectQuestion(APIView):

    def post(self,request):
        id=request.data["questionId"]
        Question.objects.all().filter(id=id).delete()

class getNotifications(APIView):
    def post(self,request):
        userId=request.data["userId"]
        notifobjs= Notifications.objects.filter(userId=userId,isSeen=False)
        count= notifobjs.count()
        notif=[] 
        for obj in notifobjs:
            notif.append(obj.msg)
            obj.isSeen=True
            obj.save()
        return JsonResponse({"notifications" : notif })

class printdata(APIView):
    def post(self,request):
        print(request.data)
        return Response(request.data)

""" class auth(APIView):
    def post(self,request):
        email=request.data["email"]
        try :
            user_obj=User.objects.filter(email=email)
        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED) """




class applicationList(APIView):
    def get(self,request):
        applications1 = applications.objects.all()
        serializer = applicationSerializers(applications1,many = True)
        return Response(serializer.data)

    def post(self,request):
        print(request.data)
        serializer = applicationSerializers(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



