from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from email.message import EmailMessage
import smtplib
from rest_framework.response import Response
from rest_framework import status

class EmailAPI(APIView):
    def post(self, request):
        subject = request.data.get('subject')
        txt_ = request.data.get('message')
        email= request.data.get('email')
        name = request.data.get('name') 
        number = request.data.get('number')
        message = request.data.get('message')
        from_email = settings.DEFAULT_FROM_EMAIL

        if subject is None or email is None:
            return Response({'msg': 'Subject and Recipient List are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if txt_ is None:
            return Response({'msg': 'Text is required.'}, status=status.HTTP_400_BAD_REQUEST)
        print('name', name)
        msg_body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nPhone Number: {number}\nMessage: {message}"
        msg = EmailMessage()
        msg.set_content(msg_body)
        msg['Subject'] = 'Booking For Conference'
        msg['From'] =email
        msg['To'] = from_email

        try:
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            return Response({'msg': 'Failed to send email.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return redirect('https://conference.uibfs.or.ug/success.html')