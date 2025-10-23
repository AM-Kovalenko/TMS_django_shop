from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

# Этот декоратор подписывает функцию на сигнал post_save модели Product
@receiver(post_save, sender=Product)
def product_created_signal(sender, instance, created, **kwargs):
    if created:
        # Если объект только что создан
        print(f"cоздан новый продукт: {instance.name}")
    else:
        # Если объект обновлён
        print(f"Обновлён продукт: {instance.name}")