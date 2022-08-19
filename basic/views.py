from array import array
from ast import Delete
from asyncio.windows_events import NULL
from urllib import response
from django.shortcuts import render
from .models import  Notifications, Question,applications,UserProfile
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.http import JsonResponse
from .serializers import QuestionSerializer,UserProfileSerializer,applicationSerializers
from django.contrib.auth import get_user_model
from django.db.models.base import ObjectDoesNotExist
User = get_user_model()
from django.conf import settings
from django.contrib.auth import login,authenticate
# Create your views here.

def index(request):
    """ User.objects.all().delete()
    UserProfile.objects.all().delete()
    Question.objects.all().delete()
    Notifications.objects.all().delete() """
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
      useremail= obj.uploadedBy
      print(type(useremail))
      print(useremail)
      if useremail != "":
        notifobj= Notifications()
        notifobj.useremail=useremail
        notifobj.quesid=id
        notifobj.msg="Your question has been verified!"
        notifobj.save() 
      return Response(status=status.HTTP_201_CREATED)

class RejectQuestion(APIView):

    def post(self,request):
        id=request.data["questionId"]
        Question.objects.all().filter(id=id).delete()

class getNotifications(APIView): #has to be tested !!!important!!!!
    def get(self,request):
        email=request.query_params["email"] ### change this to request.user 
        notifobjs= Notifications.objects.filter(useremail=email,isSeen=False).values()
        notifobjs=list(notifobjs)
        print(notifobjs)
        count= len(notifobjs)
        #return Response(status=status.HTTP_200_OK)
        return JsonResponse({"notifications" : notifobjs,"count": count})

class printdata(APIView): #tested
    def post(self,request):
        print(request.data)
        return Response(request.data)

class onetapsignin(APIView): #tested
    def post(self,request):
            email=request.data["email"]
            try:
                go = User.objects.get(email=email)
            except User.DoesNotExist:
                go = None
            if go==None:
                #id=request.data["id"]
                email=request.data["email"]
                first_name=request.data["firstName"]
                last_name=request.data["lastName"]
                userobj=User(email=email,first_name=first_name,last_name=last_name,username=email)
                userobj.save()
                user=User.objects.get(username=email)
                userid=user.id
                userProf=UserProfile(id=userid,email=email)
                userProf.save()
            user = User.objects.get(username=email)
            userid=user.id
            userprofobj=UserProfile.objects.get(id=userid,email=email)
            user.backend='django.contrib.auth.backends.ModelBackend'
            login(request, user)
            print(request.user)
                
            return Response({"id": userprofobj.id, "isVerifier" : userprofobj.isVerifier, "isAdmin" : userprofobj.isAdmin})




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

class getQuesBySubj(APIView): #has to be tested
    def get(self,request):
        subj=request.query_params["subject"]
        objs=Question.objects.filter(subject__contains=[subj],isVerified=True)
        for obj in objs:
            print(obj.question)
        return Response(status=status.HTTP_200_OK)

class addToFav(APIView): #tested
    def post(self,request):
        email=request.data["email"]
        print(email)
        print(type(email)) ##change this to request.user
        quesId=request.data["quesId"]
        userprofobjs=UserProfile.objects.get(email=email)
        #userprofobjs=userprofobjs[0]
        print(userprofobjs)
        userprofobjs.favourites.append(quesId)
        print(userprofobjs.favourites)
        userprofobjs.save()
        return Response(status=status.HTTP_202_ACCEPTED)

class removeFromFav(APIView): #tested
    def post(self,request):
        email=request.data["email"] ##change this to request.user
        quesId=request.data["quesId"]
        userprofobjs=UserProfile.objects.filter(email=email)
        userprofobjs=userprofobjs[0]
        userprofobjs.favourites.remove(quesId)
        userprofobjs.save()
        return Response(status=status.HTTP_200_OK)
class getFavs(APIView): #tested
    def get(self,request): ##get necessary fields from fe team9
        email=request.query_params["email"] ##change this to request.user
        userprofobjs=UserProfile.objects.filter(email=email)
        userprofobjs=userprofobjs[0]
        print(userprofobjs.favourites)
        favList=userprofobjs.favourites
        data=[]
        for fav in favList:
            quesobj=Question.objects.get(id=fav)
            obj={"question": quesobj.question,
                  "options": quesobj.options,
                  "answer" : quesobj.answer  }
            data.append(obj)
        print(data)
        return JsonResponse({"data" : data},safe=False)

class verifyApplications(APIView):
    def post(self,request):
        pass
class getQuesByMe(APIView):
    def get(self,request):
        userEmail = request.query_params["email"]
        questionObjects = Question.objects.filter(uploadedBy = userEmail)
        return JsonResponse(questionObjects)

class quesVerifiedByMe(APIView):
    def get(self,request):
        userEmail = request.query_params["email"]
        userObj = User.objects.filter(email = userEmail)
        amIVerified = userObj.isVerifier
        if amIVerified:
            print("as")
            listOfVerifiedQues = Question.objects.filter(verifiedBy = userEmail)
            return JsonResponse(listOfVerifiedQues)
        else:
            print("not a verifier")

