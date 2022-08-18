from asyncio.windows_events import NULL
import email
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings
#User = get_user_model()

# Create your models here.
class UserProfile(models.Model):
    id = models.IntegerField()
    email=models.CharField(max_length=255,primary_key=True)
    favourites = ArrayField(models.CharField(max_length=200),default=list)
    isAdmin = models.BooleanField(default=False)
    isVerifier = models.BooleanField(default=False)

    
class Verifier(models.Model):
    id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    questionsVerified =ArrayField(models.CharField(max_length=20))
    expertise = models.TextField()


class Question(models.Model):
    question=models.TextField()
    options=ArrayField(models.CharField(max_length=75))
    uploadedBy=models.CharField(max_length=30) #userid
    verifiedBy= models.CharField(max_length=30)
    answer=models.CharField(max_length=75)
    Class = models.CharField(max_length=20)
    isRendered = models.BooleanField(default=False)
    isRenderedat = models.DateTimeField(blank=True, null=True)
    isVerified = models.BooleanField(default=False)
    encodedValue = models.CharField(max_length=30)
    difficulty = models.IntegerField()
    subject = ArrayField(models.CharField(max_length=30))
    tags = ArrayField(models.CharField(max_length=20))
    createdAt = models.DateTimeField(auto_now_add=True)
    noOfTimesFaved = models.IntegerField(default=0)
    explanation = models.TextField(default="No explanation")
    COLevel = models.CharField(max_length=50,default="Understand")
    #optionlist : done 
    #class : done
    #subj->list done
    #ques->isrendered done
    #ques-> isrenderedat done
    #when creating user instance , create notification instance too
    #send only notif count to home[age]
class Notifications(models.Model):
    userId= models.CharField(max_length=30)
    isSeen = models.BooleanField(default=False)
    msg = models.TextField()

class applications(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    marks_10 = models.DecimalField(max_digits=5,decimal_places=1)
    marks_12 = models.DecimalField(max_digits=5,decimal_places=1)
    marks_degree = models.DecimalField(max_digits=4,decimal_places=2)
    is_teacher = models.BooleanField()
    experience = models.IntegerField()


