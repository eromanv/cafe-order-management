from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("ready", "Готов к выдаче"),
        ("paid", "Оплачен"),
    ]

    table_number = models.IntegerField()
    items = models.JSONField()  # Список блюд с ценами
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def save(self, *args, **kwargs):
        # Пересчитываем общую стоимость при сохранении
        self.total_price = sum(item["price"] for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number} - Status: {self.status}"
