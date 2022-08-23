from asyncio.windows_events import NULL
import email
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings
import numpy as np
from ndarraydjango.fields import NDArrayField

#User = get_user_model()
DATE_INPUT_FORMATS = ['%d-%m-%Y'] ### add this to application
# Create your models here.
class UserProfile(models.Model):
    id = models.IntegerField()
    email=models.CharField(max_length=255,primary_key=True)
    favourites = ArrayField(models.IntegerField(),default=list)
    isAdmin = models.BooleanField(default=False)
    isVerifier = models.BooleanField(default=False)


class encoded(models.Model):
     encodedValue =NDArrayField(shape=(1, 768), dtype=np.float32,blank=True,null=True)


class Verifier(models.Model):
    email=models.CharField(max_length=255)
    questionsVerified =ArrayField(models.IntegerField(),default=list)
    expertise = models.TextField()

#add verified-done in sameer  to
class Question(models.Model):
    question=models.TextField()
    options=ArrayField(models.CharField(max_length=75))
    uploadedBy=models.CharField(max_length=30,blank=True,null=True) #userid
    verifiedBy= models.CharField(max_length=30,blank=True,null=True)
    answer=models.CharField(max_length=75)
    Class = models.CharField(max_length=20)
    isRendered = models.BooleanField(default=False)
    isRenderedat = models.DateTimeField(blank=True, null=True)
    isVerified = models.BooleanField(default=False)
    verifiedOn=models.DateTimeField(blank=True,null=True)
    #encodedValue =NDArrayField(shape=(1, 768), dtype=np.float32,blank=True,null=True)
    difficulty = models.IntegerField()
    subject = ArrayField(models.CharField(max_length=30))
    tags = ArrayField(models.CharField(max_length=20))
    createdAt = models.DateTimeField(auto_now_add=True)
    noOfTimesFaved = models.IntegerField(default=0)
    explanation = models.TextField(default="No explanation")
    COLevel = models.CharField(max_length=50,default="Understand")
    
    #verifiedOn=models.DateField(auto_now=False,auto_now_add=True)
    #optionlist : done 
    #class : done
    #subj->list done
    #ques->isrendered done
    #ques-> isrenderedat done
    #when creating user instance , create notification instance too
    #send only notif count to home[age]
class Notifications(models.Model):
    useremail= models.CharField(max_length=30)
    isSeen = models.BooleanField(default=False)
    quesid=models.IntegerField(blank=True,null=True)
    msg = models.TextField()
    verifynotif=models.BooleanField(default=False)
    createdAt=models.DateTimeField(auto_now_add=True)

class applications(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    dob = models.DateField(auto_now=False, auto_now_add=False) ## needs to be fixed
    marks_10 = models.DecimalField(max_digits=5,decimal_places=1)
    marks_12 = models.DecimalField(max_digits=5,decimal_places=1)
    marks_degree = models.DecimalField(max_digits=4,decimal_places=2)
    is_teacher = models.BooleanField()
    experience = models.IntegerField()
    email = models.CharField(max_length=255)
    expertise=models.CharField(max_length=255)

