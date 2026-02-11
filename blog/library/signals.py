from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver, Signal
from django.contrib.auth.signals import user_logged_in
from .models import Book, Loan, Author






@receiver(post_save, sender=Book)
def book_pre_save(sender, instance, **kwargs):
    if instance.title:
        instance.title = instance.title.strip()
        print("testtt")


@receiver(post_save, sender=Book)
def book_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"cigni sheikmna carmatebit {instance.title} avtoria {instance.author}")
    else:
        print(f"########## cigni shvecvalet carmatebit {instance.title}")


@receiver(post_delete, sender=Book)
def book_post_delete(sender, instance, **kwargs):
    print(f"cigni caishala {instance.title}")

    if instance.cover:
        instance.cover.delete(save=False)

@receiver(post_save, sender=Loan)
def loan_created(sender, instance, created, **kwargs):
    if created:
        print(f"cigni caigo: {instance.book.title} studentma")


@receiver(pre_save, sender=Loan)
def loan_returned(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_loan = Loan.objects.get(pk=instance.pk)
            if old_loan.returned_at is None and instance.returned_at is not None:
                print(f"cigni dabrunebulia {instance.book.title}")
                print(f"studentis saxeli: {instance.student}")

        except Loan.DoesNotExist:
            print(f"cigni ar caugia aravis")

