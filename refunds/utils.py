from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_refund_status_email(refund_request):
    """
Sends an email with information about the updated status of the request.
Uses an HTML template and a text version.
"""
    subject = f"Status of your request #{refund_request.id} changed"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [refund_request.email]

    # Text version of the letter (fallback for clients without HTML)
    text_content = (
        f"Hello, {refund_request.first_name}!\n\n"
        f"The status of your refund request #{refund_request.id} "
        f"(order number: {refund_request.order_number}) has been changed to '{refund_request.status}'."
    )

    # HTML version of the letter
    html_content = render_to_string(
        'emails/refund_status.html',  # Path to template
        {'refund': refund_request}    # Context for the template
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")  # Attach the HTML version
    msg.send()
