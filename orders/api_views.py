from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["status", "table_number"]
    search_fields = ["table_number", "status"]
    ordering_fields = ["id", "table_number", "total_price"]

    @action(detail=False, methods=["get"])
    def stats(self, request):
        total_orders = Order.objects.count()
        total_revenue = sum(
            order.total_price for order in Order.objects.filter(status="paid")
        )
        by_status = {
            status: Order.objects.filter(status=status).count()
            for status, _ in Order.STATUS_CHOICES
        }

        return Response(
            {
                "total_orders": total_orders,
                "total_revenue": total_revenue,
                "by_status": by_status,
            }
        )
