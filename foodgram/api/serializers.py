from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from recipes.models import FollowUser, User


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowUser
        fields = ("id", "following_user_id")


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = ("id", "user_id")


class UserSerializer(serializers.ModelSerializer):

    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "following",
            "followers"
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data
