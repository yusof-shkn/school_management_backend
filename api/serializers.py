from rest_framework import serializers
from .models import User
from .models import Student
from .models import Teacher
from .models import Class

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','schoolName','schoolEmail']
        
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class_name = serializers.SerializerMethodField() 
 
    class Meta: 
        model = Teacher 
        fields = ['id', 'name', 'lname', 'phnum', 'subject', 'email', 'gender', 'photo', 'class_id', 'class_name', 'user'] 
 
    def get_class_name(self, obj): 
        return obj.class_id.name if obj.class_id else None 


class StudentSerializer(serializers.ModelSerializer):
    class_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'phnum', 'email', 'gender', 'photo', 'class_id', 'class_name', 'user']

    def get_class_name(self, obj):
        return obj.class_id.name if obj.class_id else None
        

