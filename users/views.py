import random
from dj_rest_auth.serializers import PasswordChangeSerializer
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from allauth.account.models import EmailAddress
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from users.permessions import IsOwnerOrReadOnly
from users.serializers import RegisterSerializer, CodeSerializer, GetEmailSerializer, UserSerializer
from users.models import ChangedPassword, Code
from users.serializer import LogOutSerializer
from users.utils import send_email
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

User = get_user_model()

class UserViewSet(RetrieveModelMixin, ListAPIView, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    # permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ("username", "first_name", "last_name")
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def list(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        if not username:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = self.get_queryset().filter(username=username).first()
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def me(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        check = self.check_user_verify(request)
        if serializer.is_valid(raise_exception=True):
            if check:
                serializer.save()
            else:
                return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            code, created = Code.objects.get_or_create(user_id=serializer.data['id'])
            code.save()
            send_email({'to_email': serializer.data['email'], 'code': code.number})
            # Todo: send the code by email to user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_user_verify(self, request):
        try:
            email = request.data.get('email')
        except:
            return True
        if not EmailAddress.objects.filter(email=email).first():
            user = User.objects.filter(email=email)
            user.delete()
            return True
        else:
            return False


class VerifyCodeView(generics.GenericAPIView):
    serializer_class = CodeSerializer
    permission_classes = (AllowAny,)
    queryset = Code.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            num = Code.objects.filter(user_id=int(serializer.data['user'])).first()
            if not num:
                return Response({'error': 'code not found'}, status=status.HTTP_400_BAD_REQUEST)
            if str(num.number) == str(serializer.data['number']):
                user = User.objects.filter(id=int(serializer.data['user'])).first()
                EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
                token = self.get_tokens_for_user(user)
                login(request, user)
                return Response({'Message': 'Successfully activated', 'token': token}, status=status.HTTP_200_OK)
            return Response({'Message': 'Code is not match'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutSerializer

    def post(self, request, *args, **kwargs):
        serializer = LogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.data['refresh'])
        except:
            return Response({'message': "Token is blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)


class PasswordChangeView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    throttle_scope = 'dj_rest_auth'

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get("new_password1") == serializer.data.get("new_password2"):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(viewsets.ModelViewSet):
    queryset = ChangedPassword.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetEmailSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = self.generate_password()
            user = User.objects.filter(email=serializer.data['email']).first()
            if not user:
                return Response(status=status.HTTP_404_NOT_FOUND)
            changed_users = ChangedPassword.objects.filter(user=user).first()
            if changed_users:
                changed_users.password = password
                changed_users.save()
            else:
                ChangedPassword.objects.create(user=user, password=password)
            user.set_password(password)
            user.save()
            send_email({'to_email': serializer.data['email'], 'code': password})
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def generate_password(self):
        signs = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
        password = ''
        for i in range(10):
            num = random.choice(signs)
            password += str(chr(num))
        return password
