from rest_framework import serializers
from apps.expenditure.models import SchoolExpenditure

class SchoolExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolExpenditure
        fields = ["id", "item_name", "category", "amount", "transaction_date", "paid_to"]

