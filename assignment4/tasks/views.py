from django.shortcuts import render
from django.http import JsonResponse
from .models import Email
from .tasks import send_email_task

def send_email_view(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        email = Email.objects.create(recipient=recipient, subject=subject, body=body)
        send_email_task.delay(recipient, subject, body)

        return JsonResponse({'status': 'Email is being sent in the background.'})

    return render(request, 'send_email.html')
