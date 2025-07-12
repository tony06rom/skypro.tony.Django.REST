from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.url = field

    def __call__(self, fields):
        if fields.get("video_url"):
            if "youtube.com" not in fields["video_url"]:
                raise ValidationError("Разрешены только ссылки на YouTube")
