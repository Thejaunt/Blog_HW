from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template import loader


@shared_task()
def email_contact_task(user_email, subject, text, from_email, recipient_list):
    message = loader.render_to_string("blog/email-contact-us.html", {"message": text, "user_email": user_email})
    msg = EmailMessage(
        subject=subject or "contact us",
        body=message,
        from_email=from_email,
        to=recipient_list,
    )
    msg.content_subtype = "html"
    msg.send(fail_silently=False)


@shared_task()
def email_new_record(subject, text, from_email, recipient_list):
    subject = subject or "New record"
    message = loader.render_to_string("blog/email_new_comment_post.html", {"message": text})
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
