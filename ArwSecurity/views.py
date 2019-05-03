import self as self
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets, request, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, BaseAuthentication, \
    TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from ArwSecurity.models import product
from ArwSecurity.serializers import ProductSerializer, UserSerializer, GroupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

@csrf_exempt
def user_list(request):
    """
      List all code snippets, or create a new snippet.
      """
    if request.method == 'GET':
        try:

            token = request.META['HTTP_AUTHORIZATION']

        except Exception as e:
            return JsonResponse({"detail": "Authentication credentials were not provided"}, status=401)

        print("eltoken "+token)
        parts = token.split(" ")

        if token == "":
            return JsonResponse({"detail": "Invalid token."}, status=401)
        else:
            try:
                token = Token.objects.get(key=parts[1])
            except Token.DoesNotExist:
                return JsonResponse({"detail": "Invalid credentials."}, status=401)

            print(token.user_id)
            user = User.objects.get(id=token.user_id)
            if user.is_staff:

             users = User.objects.all().values('username', 'email',"date_joined")  # or simply .values() to get all fields
             users_list = list(users)  # important: convert the QuerySet to a list object
             return JsonResponse(users_list, safe=False)
            else:
                return JsonResponse({"detail": "Unauthorized"}, status=401)


    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class UserViewSet(viewsets.ModelViewSet):

            queryset = User.objects.all()
            serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
