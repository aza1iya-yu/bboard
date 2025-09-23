from rest_framework import serializers

from main.models import Bb, Comment


class BbListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = (
            "id",
            "title",
            "content",
            "price",
            "created_at",
        )


class BbDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = (
            "id",
            "title",
            "content",
            "price",
            "created_at",
            "contacts",
            "image",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "bb",
            "author",
            "content",
            "created_at",
        )
