from rest_framework import serializers
from .models import Course, Lesson, CourseSubscription
from .validators import youtube_link_validator


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count", "owner", "is_subscribed"]  # ← +is_subscribed

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        """Подписан ли текущий пользователь на курс?"""
        user = self.context['request'].user
        if user.is_authenticated:
            return CourseSubscription.objects.filter(
                user=user, course=obj
            ).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    video_link = serializers.URLField(
        validators=[youtube_link_validator],
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "video_link", "owner"]