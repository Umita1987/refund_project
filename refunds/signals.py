from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import RefundRequest
from .utils import send_refund_status_email


@receiver(pre_save, sender=RefundRequest)
def send_status_update_notification(sender, instance, **kwargs):
    # If this is a new entry, we do not send the letter.
    if not instance.pk:
        return

    try:
        previous = RefundRequest.objects.get(pk=instance.pk)
    except RefundRequest.DoesNotExist:
        return

    # If the status has changed, we send a letter through our function
    if previous.status != instance.status:
        send_refund_status_email(instance)