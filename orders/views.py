from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
import logging
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)


def order_list(request):
    """
    Отображает список заказов с возможностью фильтрации по статусу.
    """
    orders = Order.objects.all().order_by("id")
    status_filter = request.GET.get("status")

    if status_filter:
        orders = orders.filter(status=status_filter)

    context = {
        "orders": orders,
        "status_choices": Order.STATUS_CHOICES,
        "current_status": status_filter,
    }
    return render(request, "orders/order_list.html", context)


def order_detail(request, order_id):
    """
    Отображает детали конкретного заказа.
    """
    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "status_choices": Order.STATUS_CHOICES,
        },
    )


def order_create(request):
    """
    Создает новый заказ. Если метод запроса POST, сохраняет заказ
    и перенаправляет на список заказов.
    """
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.status = "pending"
                order.save()
                logger.info(f"Order created: {order.id}")
                return redirect("order_list")
            except Exception as e:
                logger.error(f"Error creating order: {str(e)}")
                form.add_error(None, f"Error saving order: {str(e)}")
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = OrderForm()
    return render(request, "orders/order_form.html", {"form": form})


def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.save()
                return HttpResponseRedirect("/orders/")
            except Exception as e:
                logger.error(f"Error updating order: {str(e)}")
                form.add_error(None, f"Error updating order: {str(e)}")
    else:
        form = OrderForm(instance=order)
        form.initial["items"] = order.items
    return render(request, "orders/order_form.html", {"form": form})


def order_delete(request, order_id):
    """
    Удаляет существующий заказ. Если метод запроса POST,
    удаляет заказ и перенаправляет на список заказов.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")
    return render(request, "orders/order_confirm_delete.html", {"order": order})


def order_search(request):
    """
    Ищет заказы по номеру стола или статусу.
    """
    query = request.GET.get("q")
    from django.db.models import Q

    orders = Order.objects.filter(
        Q(table_number__icontains=query) | Q(status__icontains=query)
    )
    return render(request, "orders/order_list.html", {"orders": orders})


def calculate_revenue(request):
    """
    Рассчитывает общий доход от оплаченных заказов.
    """
    paid_orders = Order.objects.filter(status="paid")
    total_revenue = sum(order.total_price for order in paid_orders)
    return render(request, "orders/revenue.html", {"total_revenue": total_revenue})
