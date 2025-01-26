from django import forms
from .models import Order
import json
import logging

logger = logging.getLogger(__name__)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number", "items", "status"]

    def clean_items(self):
        items = self.cleaned_data.get("items")
        try:
            if isinstance(items, str):
                items_data = json.loads(items)
            else:
                items_data = items
            if not isinstance(items_data, list):
                raise forms.ValidationError("JSON должен быть списком")

            for item in items_data:
                if not isinstance(item, dict):
                    raise forms.ValidationError("Каждый элемент должен быть объектом")
                if "name" not in item or "price" not in item:
                    raise forms.ValidationError(
                        "Каждый элемент должен содержать name и price"
                    )
                try:
                    float(item["price"])
                except (TypeError, ValueError):
                    raise forms.ValidationError("Price должен быть числом")

            return items_data
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Неверный формат JSON: {str(e)}")
