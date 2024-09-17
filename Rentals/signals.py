# Rentals/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Tenant, House

@receiver(post_save, sender=Tenant)
def update_house_vacancy_on_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # When a Tenant is created, mark the house as not vacant
        house = instance.house
        house.is_vacant = False
        house.save()
    else:
        # When a Tenant is updated, check if the house has changed
        old_tenant = Tenant.objects.get(pk=instance.pk)
        if old_tenant.house != instance.house:
            # Mark old house as vacant
            old_house = old_tenant.house
            old_house.is_vacant = True
            old_house.save()
            # Mark new house as not vacant
            new_house = instance.house
            new_house.is_vacant = False
            new_house.save()

@receiver(post_delete, sender=Tenant)
def update_house_vacancy_on_delete(sender, instance, **kwargs):
    house = instance.house
    house.is_vacant = True
    house.save()
