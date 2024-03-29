from attr import field
from rest_framework import serializers
from .models import Question, UserProfile,applications
from django.contrib.auth.models import User
from sentence_transformers import SentenceTransformer



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields=('question','options','uploadedBy','encodedValue','answer','Class','subject','tags','difficulty','explanation','COLevel')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields=('username','email','password','favourites','isAdmin','isVerfier')
class applicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = applications
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'