from wagtail import hooks
from .views import OrderViewSet

@hooks.register("register_admin_viewset")
def register_order_viewset():
    return OrderViewSet()
