from urllib.parse import urlparse
from rest_framework import serializers

def youtube_link_validator(value):
    """Проверяет, что ссылка только с youtube.com"""
    parsed = urlparse(value)
    if parsed.netloc not in ['youtube.com', 'www.youtube.com', 'youtu.be']:
        raise serializers.ValidationError(
            "Ссылка должна быть только с YouTube!"
        )