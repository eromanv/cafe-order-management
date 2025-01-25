from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("order/new/", views.order_create, name="order_create"),
    path("order/<int:order_id>/edit/", views.order_update, name="order_update"),
    path("order/<int:order_id>/delete/", views.order_delete, name="order_delete"),
    path("order/search/", views.order_search, name="order_search"),
    path("revenue/", views.calculate_revenue, name="calculate_revenue"),
]
