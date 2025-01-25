from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Список продуктов пустой.")
        return value
    class Meta:
        model = Order
        fields = [
            "id",
            "table_number",
            "items",
            "total_price",
            "status",
            "status_display",
        ]
        read_only_fields = ["total_price"]
