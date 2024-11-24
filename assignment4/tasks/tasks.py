from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True, max_retries=3)
def send_email_task(self, recipient, subject, body):
    try:
        send_mail(
            subject,
            body,
            'your_email@example.com',
            [recipient],
            fail_silently=False,
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)
