from celery import shared_task
from django.core.mail import send_mail

from config import settings
from lms.models import Course, Subscription


@shared_task
def send_mail_update_course(course_pk):
    course = Course.objects.get(pk=course_pk)
    subject = f"Курс '{course.title}' обновлен."
    message = (
        f"Автоматическая рассылка для подписчиков курса: '{course.title}'\nПожалуйста, не отвечайте на это письмо"
    )
    subs = Subscription.objects.filter(course=course)
    recipient_list = []
    for recipient in subs:
        recipient_list.append(recipient.user.email)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
    return "Сообщение отправлено"
