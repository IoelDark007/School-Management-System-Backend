from django.db import models


class SchoolExpenditure(models.Model):
    class Category(models.TextChoices):
        UTILITY = "utility"
        SUPPLIES = "supplies"
        MAINTENANCE = "maintenance"
        AMENITIES = "amenities"

    item_name = models.CharField(max_length=255)
    category = models.CharField(max_length=15, choices=Category.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateField()
    paid_to = models.CharField(max_length=255)

    class Meta:
        db_table = "school_expenditures"

    def __str__(self):
        return f"{self.item_name} - {self.amount}"
