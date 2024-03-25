from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings

class User(AbstractUser):
    password = models.CharField(max_length=255)
    schoolName = models.CharField(max_length=255)
    schoolEmail = models.CharField(max_length=255,blank=True, null=True)
    schoolImage = models.ImageField(upload_to='users/', blank=True, null=True)

    REQUIRED_FIELDS = []


class Class(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='classes/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Class: {self.name} - User: {self.user}'

    def deleted(self, *args, **kwargs):

        Teacher.objects.filter(class_id=self).delete()
        Student.objects.filter(class_id=self).delete()

        super(Class, self).delete(*args, **kwargs)

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phnum = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self): 
        if self.photo: 
            return f'{settings.MEDIA_URL}{self.photo.name}' 
        return ''

    def __str__(self):
        return f'Teacher: {self.name} - User: {self.user}'

class Student(models.Model):
    name = models.CharField(max_length=100)
    phnum = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Student: {self.name} - User: {self.user}'
