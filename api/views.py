from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .serializers import StudentSerializer
from .serializers import TeacherSerializer
from .serializers import ClassSerializer
from .models import User
from .models import Student
from .models import Teacher
from .models import Class
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import jwt, datetime
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import random
from django.http import HttpResponse
from django.db.models import Q


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return Response(False)
    except jwt.InvalidTokenError:
        return Response(False)


class RegisterView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        password = request_data.pop("password", None)

        if password:
            hashed_password = make_password(password)
            request_data["password"] = hashed_password

        serializer = UserSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        if saved:
            return Response(True)
        else:
            return Response(False)


class LoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)
        if not user:
            return Response(False)

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=600000),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        response = Response()
        response.data = {
            "token": token,
            "name": user.username,
            "schoolName": user.schoolName,
        }

        return response


class LogoutView(APIView):
    def post(self, request):
        c_token = request.data["token"]
        payload = verify_jwt_token(c_token)
        user_id = payload.get("id")
        if user_id:
            return Response(True)
        else:
            return Response(False)


class UserView(APIView):
    def post(self, request):
        c_token = request.data["token"]
        payload = verify_jwt_token(c_token)
        user_id = payload.get("id")
        user = User.objects.filter(id=user_id).first()
        if user:
            return Response(user.name)
        else:
            return Response(False)


################################################ class view ######################################################


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def list(self, request):
        token = request.GET.get("token")
        if token:
            payload = verify_jwt_token(token)
            user_id = payload.get("id")
            user = User.objects.filter(id=user_id).first()
            if user:
                search = request.GET.get("search")

                if search:
                    queryset = Class.objects.filter(
                        Q(user_id= user.id) & (Q(name__icontains=search)
                        | Q(room__icontains=search)
                        | Q(grade__icontains=search))
                    )
                    if queryset.count() == 0:
                        return Response(False)
                else:
                    queryset = Class.objects.filter(user_id=user.id)
                    if queryset.count() == 0:
                        return Response(False)

                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response(False)
        else:
            return Response(False)

    def create(self, request):
        request_data = request.data.copy()

        c_token = request.data.get("token")
        payload = verify_jwt_token(c_token)
        user_id = payload.get("id")
        user = User.objects.filter(id=user_id).first()

        request_data["user"] = user.id
        serializer = self.get_serializer(data=request_data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.errors)
        saved = serializer.save()

        if saved:
            return Response(True)
        else:
            return Response(False)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        deleted = instance.delete()
        if deleted:
            return Response(True)
        else:
            return Response(False)


################################################ teacher view ######################################################


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def list(self, request):
        token = request.GET.get("token")
        if token:
            payload = verify_jwt_token(token)
            user_id = payload.get("id")
            user = User.objects.filter(id=user_id).first()
            if user:
                search = request.GET.get("search")
                if search:
                    queryset = Teacher.objects.filter(
                        Q(user_id = user.id) & (Q(name__icontains=search)
                        | Q(lname__icontains=search)
                        | Q(email__icontains=search))
                    )
                    if queryset.count() == 0:
                        return Response(False)
                else:
                    queryset = Teacher.objects.filter(user_id=user.id)
                    if queryset.count() == 0:
                        return Response(False)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response(False)
        else:
            return Response(False)

    def create(self, request):
        request_data = request.data.copy()

        c_token = request.data.get("token")
        payload = verify_jwt_token(c_token)
        user_id = payload.get("id")
        user = User.objects.filter(id=user_id).first()

        request_data["user"] = user.id
        serializer = self.get_serializer(data=request_data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.errors)
        saved = serializer.save()

        if saved:
            return Response(True)
        else:
            return Response(False)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        deleted = instance.delete()
        if deleted:
            return Response(True)
        else:
            return Response(False)


################################################ student view ######################################################


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def list(self, request):
        token = request.GET.get("token")
        if token:
            payload = verify_jwt_token(token)
            user_id = payload.get("id")
            user = User.objects.filter(id=user_id).first()
            if user:
                search = request.GET.get("search")
                if search:
                    queryset = Student.objects.filter(
                        Q(user_id= user.id) & (Q(name__icontains=search)
                        | Q(email__icontains=search))
                    )
                    if queryset.count() == 0:
                        return Response(False)
                else:
                    queryset = Student.objects.filter(user_id=user.id)
                    if queryset.count() == 0:
                        return Response(False)

                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response(False)
        else:
            return Response(False)

    def create(self, request):
        request_data = request.data.copy()

        c_token = request.data.get("token")
        payload = verify_jwt_token(c_token)
        user_id = payload.get("id")
        user = User.objects.filter(id=user_id).first()

        request_data["user"] = user.id
        serializer = self.get_serializer(data=request_data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.errors)
        saved = serializer.save()

        if saved:
            return Response(True)
        else:
            return Response(False)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        deleted = instance.delete()
        if deleted:
            return Response(True)
        else:
            return Response(False)


################################################ for seeding ######################################################


def Seeder(request):

    for i in range(10):
        class_instance = Class.objects.create(
            name=f"Class {random.randint(1, 100)}",
            grade=str(random.randint(1, 10)),
            room=str(random.randint(1, 100)),
            photo="classes/FOR_FACEBOOK.jpg",
            user_id=6,
        )
        for j in range(5):
            teacher_instance = Teacher.objects.create(
                name=f"Teacher {random.randint(1, 100)}",
                lname=f"LastName {random.randint(1, 100)}",
                phnum=f"{random.randint(1000000000, 9999999999)}",
                subject=random.choice(["Math", "Science", "History"]),
                email=f"teacher{random.randint(1, 100)}@school.com",
                gender=random.choice(["male", "female"]),
                class_id=class_instance,
                photo="classes/FOR_FACEBOOK.jpg",
                user_id=6,
            )
        for k in range(30):
            student_instance = Student.objects.create(
                name=f"Student {random.randint(1, 100)}",
                phnum=f"{random.randint(1000000000, 9999999999)}",
                email=f"student{random.randint(1, 100)}@school.com",
                gender=random.choice(["male", "female"]),
                class_id=class_instance,
                photo="classes/FOR_FACEBOOK.jpg",
                user_id=6,
            )

    if class_instance and student_instance and teacher_instance:
        return HttpResponse([{"operation": "True"}])
    else:
        return HttpResponse([{"operation": "False"}])


################################################ for Delete all ######################################################


def delete_all(request):

    classes = Class.objects.all().delete()

    teachers = Teacher.objects.all().delete()

    students = Student.objects.all().delete()

    if classes and students and teachers:
        return HttpResponse([{"operation": "True"}])
    else:
        return HttpResponse([{"operation": "False"}])


# def update(self, request, pk=None):
#     instance = self.get_object()
#     serializer = self.get_serializer(instance, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)

# def partial_update(self, request, pk=None):
#     instance = self.get_object()
#     serializer = self.get_serializer(instance, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
# class TeacherViewSet(APIView):
#     def post(self, request):
#         request_data = request.data.copy()

#         c_token = request.data.get('token')
#         payload = verify_jwt_token(c_token)
#         user_id = payload.get('id')
#         user = User.objects.filter(id=user_id).first()

#         request_data['user'] = user.id
#         serializer = TeacherSerializer(data=request_data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except Exception as e:
#             print(serializer.errors)
#         saved = serializer.save()

#         if saved:
#             return Response(True)
#         else:
#             return Response(False)
# class RecordView(APIView):
#     def post(self, request):

#         c_token = request.data['token']
#         payload = verify_jwt_token(c_token)
#         user_id = payload.get('id')
#         user = User.objects.filter(id=user_id).first()
#         typingTests = TypingTest.objects.filter(user_id = user.id)[:5]
#         serializer = TypingTestSerializer(typingTests,many=True)

#         if(user):
#             return Response(serializer.data)
#         else:
#             return Response(False)

# class RecordSave(APIView):
#     def post(self, request):

#         newWpm = request.data['WPM']
#         c_token = request.data['token']
#         print(newWpm,c_token)
#         payload = verify_jwt_token(c_token)
#         user_id = payload.get('id')
#         user = User.objects.filter(id=user_id).first()
#         saveWpm = TypingTest(user_id = user.id,wpm = newWpm)
#         saveWpm.save()

#         if(user):
#             return Response(True)
#         else:
#             return Response(False)
