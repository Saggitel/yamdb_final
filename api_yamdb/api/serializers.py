from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


def validate_username(value):
    if value == 'me':
        raise serializers.ValidationError('недопустимое имя пользователя')
    return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(max_length=150,
                                     validators=(validate_username, ))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)

    def validate(self, data):
        if User.objects.filter(Q(email=data.get('email'))
                               | Q(username=data.get('username'))).exists():
            raise serializers.ValidationError(
                {'user': 'Такой пользователь уже существует'})
        return data


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(write_only=True,
                                     max_length=150,
                                     validators=(validate_username, ))
    confirmation_code = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        user = get_object_or_404(
            User, username=self.validated_data['username'])
        confirmation_code = self.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            return str(AccessToken.for_user(user))
        # error!

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {'confirmation_code': 'неверный проверочный код'})
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleGETSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=True
    )
    rating = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )
    title = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять более одного отзыва к произведению.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )
    review = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
