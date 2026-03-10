from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # fields = "__all__","lessons_count"
        fields = ["id", "title", "description", "lessons_count"]

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        # fields = "__all__"
        fields = ["id", "title", "description"]
