from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.url = field

    def __call__(self, fields):
        if not 'youtube.com' in fields['video_url']:
            raise ValidationError('Разрешены только ссылки на YouTube')
