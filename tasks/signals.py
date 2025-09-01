from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task


@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]

        send_mail(
            "New employee joined",
            "New employee.",
            "avijitroy926avijit@gmail.com",
            assigned_emails,
            fail_silently=False,
        )
