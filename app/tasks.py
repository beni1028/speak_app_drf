from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_email(email):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=email,is_active=False)
    except UserModel.DoesNotExist:
        return None
    try:
        subject = 'Verify Your Account'
        html_message = f"Please click on the link to activate: http:/localhost:8000/verify_account/?aid={user.aid}"
        from_email = 'noreply@example.com'
        to_email = user.email
        send_mail(subject, html_message, from_email, [to_email])
        return True
    except Exception as err:
        print(f"Excption came while trying to send activation email. Error:{err}")
        return False