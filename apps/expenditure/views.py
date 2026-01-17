from rest_framework import viewsets
from apps.expenditure.models import SchoolExpenditure
from apps.expenditure.serializers import SchoolExpenditureSerializer
from rest_framework.permissions import IsAuthenticated

class SchoolExpenditureViewSet(viewsets.ModelViewSet):
    queryset = SchoolExpenditure.objects.all()
    serializer_class = SchoolExpenditureSerializer
    permission_classes = [IsAuthenticated]

