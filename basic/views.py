from array import array
from ast import Delete
from asyncio.windows_events import NULL
from urllib import response
from django.shortcuts import render
from .models import  Notifications, Question,applications,UserProfile,Verifier
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.http import JsonResponse,FileResponse
from .serializers import QuestionSerializer,UserProfileSerializer,applicationSerializers
from django.contrib.auth import get_user_model
from django.db.models.base import ObjectDoesNotExist
User = get_user_model()
from django.conf import settings
from django.contrib.auth import login,authenticate
import datetime
# Create your views here.

def index(request):
    """ User.objects.all().delete()
    UserProfile.objects.all().delete()
    Question.objects.all().delete()
    Notifications.objects.all().delete()"""
    applications.objects.all().delete() 
    return  render(request,'index.html')


class CreateQuestionview(APIView): #tested
  
  def post(self,request):
    #temp=request.data
    print(request.data)
    serializer = QuestionSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FetchRecentQuestions(APIView): #recent
  def get(self,request):
        queryset=Question.objects.all().filter(isVerified=True)
        queryset=queryset.order_by('-createdAt')[:10]
        loggedin=request.query_params["loggedin"]
        
        if loggedin == False:
            queryset=list(queryset.values())
            return  JsonResponse(queryset,safe=False)
        if loggedin == True: 
            email=request.query_params["email"]
            profobj=UserProfile.objects.get(email=email)
            favList=profobj.favourites
            data=[]
            for obj in queryset:
                fav=False
                if obj.id in favList:
                    fav=True
                temp = { "question" : obj.question,
                        "options" : obj.options,
                        "answer" : obj.answer,
                        "difficulty" : obj.difficulty,
                        "subject" : obj.subject,
                        "tags" : obj.tags,
                        "isFav" : fav}
                data.append(temp)
            return JsonResponse({"data" : data},safe=False)
        



class quesStatus(APIView):
    def get(self,request):
        quesId = request.query_params["id"]
        quesObj = Question.objects.get(id = quesId)
        isVerified = quesObj.isVerified
        #question = list(Question.objects.filter(id = quesId).values())
        if isVerified:
            data = []
            obj = {
                "isVerified" : quesObj.isVerified,
                "VerifiedBY" : quesObj.verifiedBy,
                "VerifiedOn" : quesObj.verifiedOn,
            }
            data.append(obj)
            return JsonResponse({"data" : data},safe = False)
        else:
            data = []
            obj = {
                "isVerfied" : quesObj.isVerified,
            }
            data.append(obj)
            return JsonResponse({"data" : data},safe = False)
class VerifyQuestion(APIView):
#add verifeied on---done
#send email
#django testing done
    def post(self,request):
      id=request.data["questionId"]
      obj=Question.objects.get(id=id)
      obj.isVerified=True
      obj.verifiedBy = request.data["verifierId"]
      obj.verifiedOn=datetime.datetime.now()
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
        #print(request.FILES)
        return FileResponse(request.FILES)

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

class getQuesBySubj(APIView): #tested----do this
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
        quesobj=Question.objects.get(id=quesId)
        quesobj.noOfTimesFaved=quesobj.noOfTimesFaved+1
        quesobj.save()
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
                  "answer" : quesobj.answer,
                  "COLevel" : quesobj.COLevel }
            data.append(obj)
        print(data)
        return JsonResponse({"data" : data},safe=False)

class verifyApplications(APIView): #needs to be tested
    #send email
    def post(self,request):
        id=request.data["applicationId"]
        appobj=applications.objects.get(id=id)
        email=appobj.email
        print(email)
        userprofobj=UserProfile.objects.get(email=email)
        userprofobj.isVerifier=True
        userprofobj.save()
        expertise=appobj.expertise
        verifobj = Verifier(expertise=expertise,email=email)
        verifobj.save()
        notifobj= Notifications(useremail=email,msg="Your application has been accepted",verifynotif=True)
        notifobj.save()
        return Response(status=status.HTTP_202_ACCEPTED)

class getQuesByMe(APIView): #tested
    def get(self,request):
        userEmail = request.query_params["email"]
        questionObjects = list(Question.objects.filter(uploadedBy = userEmail).values())
        print(questionObjects)
        return JsonResponse(questionObjects,safe = False)

class quesVerifiedByMe(APIView): #tested
    def get(self,request):
        userEmail = request.query_params["email"]
        listOfVerifiedQues = list(Question.objects.filter(verifiedBy = userEmail).values())
        return JsonResponse(listOfVerifiedQues,safe=False)

class checkemail(APIView): #tested
    def get(self,request):
        email = request.query_params["email"]
        try:
                go = User.objects.get(email=email)
        except User.DoesNotExist:
                go = None
        if go==None:
            flag = False
        else:
            flag= True
        return JsonResponse({"exists" : flag},safe = False)



