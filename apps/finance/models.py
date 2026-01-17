from django.db import models
from apps.profiles.models import Student


class FeeCategory(models.Model):
    category_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "fee_categories"
        verbose_name_plural = "fee categories"

    def __str__(self):
        return f"{self.category_name} - {self.amount}"


class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = "unpaid"
        PARTIAL = "partial"
        PAID = "paid"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="invoices")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UNPAID)

    class Meta:
        db_table = "invoices"

    def __str__(self):
        return f"Invoice #{self.id} - {self.student}"


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "cash"
        BANK_TRANSFER = "bank_transfer"
        CARD = "card"

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=15, choices=Method.choices)
    transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment #{self.id} - {self.amount_paid}"
