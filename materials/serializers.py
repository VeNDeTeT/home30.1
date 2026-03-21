from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count", "owner"]

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "owner"]
