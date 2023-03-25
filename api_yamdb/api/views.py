from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, generics
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsUserAdminModeratorOrReadOnly)
from .send_email import send_code
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateTokenSerializer, GenreSerializer,
                          ReviewSerializer, TitleGETSerializer,
                          TitleSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User, username=self.request.user.username)

    def perform_update(self, serializer):
        if (self.request.user.is_admin
            or self.request.user.is_staff
                or self.request.user.is_superuser):
            serializer.save()
        else:
            serializer.save(role=self.request.user.role)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=serializer.data.get('username'),
            email=serializer.data.get('email')
        )
        confirmation_code = default_token_generator.make_token(user)
        send_code(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsUserAdminModeratorOrReadOnly,
    )

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsUserAdminModeratorOrReadOnly,
    )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
