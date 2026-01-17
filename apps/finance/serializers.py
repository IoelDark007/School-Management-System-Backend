from rest_framework import serializers
from apps.finance.models import Invoice, Payment
from apps.profiles.serializers import StudentSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "invoice", "amount_paid", "method", "transaction_date"]

class InvoiceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ["id", "student", "total_amount", "due_date", "status", "payments"]

