from django.template.loader import render_to_string
from django.core.signing import Signer

signer = Signer()


def send_activation_notification(request, user):
    context = {
        "protocol": request.scheme,
        "user": user,
        "host": request.get_host(),
        "sign": signer.sign(user.username),
    }
    subject = render_to_string("emails/activation_letter_subject.txt", context)
    body_text = render_to_string("emails/activation_letter_body.txt", context)
    user.email_user(subject, body_text)
