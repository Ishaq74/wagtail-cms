from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.panels import FieldPanel, InlinePanel
from .models import Order, OrderLine
from wagtail.models import LockableMixin, RevisionMixin, PreviewableMixin
from django.http import HttpResponse

class OrderViewSet(LockableMixin, RevisionMixin, PreviewableMixin, ModelViewSet):
    model = Order
    name = "order"
    menu_label = "Commandes"
    menu_icon = "doc-full-inverse"
    icon = "doc-full-inverse"
    menu_order = 200
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("id", "customer_name", "email", "status", "", "created_at")
    search_fields = ("id", "customer_name", "email", "status")
    form_fields = [
        "customer_name",
        "email",
        "order_date",
        "billing_address",
        "shipping_address",
        "local_total_ht",
        "local_total_tva",
        "local_total_ttc",
        "foreign_total_ht",
        "foreign_total_tva",
        "foreign_total_ttc",
        "shipping_option",
        "shipping_cost",
        "shipping_label",
        "country",
        "status",
        "is_invoiced",
        "is_payed",
        "lines",
    ]
    list_filter = (
        "status",
        "country",
        "created_at",
    )

    panels = [
        FieldPanel('customer_name'),
        FieldPanel('email'),
        FieldPanel('billing_address'),
        FieldPanel('shipping_address'),
        FieldPanel('local_total_ht'),
        FieldPanel('local_total_tva'),
        FieldPanel('local_total_ttc'),
        FieldPanel('foreign_total_ht'),
        FieldPanel('foreign_total_tva'),
        FieldPanel('foreign_total_ttc'),
        FieldPanel('shipping_option'),
        FieldPanel('shipping_cost'),
        FieldPanel('shipping_label'),
        FieldPanel('country'),
        FieldPanel('status'),
        FieldPanel('is_invoiced'),
        FieldPanel('is_payed'),
        InlinePanel('lines', label="Lignes de commande"),
    ]

    def get_queryset(self, request):
        """
        Méthode permettant de filtrer les commandes selon l'utilisateur ou autres critères si nécessaire.
        """
        queryset = super().get_queryset(request)
        return queryset

    def preview(self, request, *args, **kwargs):
        """
        Méthode personnalisée pour la prévisualisation.
        """
        instance = self.get_object(request, *args, **kwargs)
        context = {
            'order': instance,
            'lines': instance.lines.all(),
            'local_total_ht': instance.local_total_ht,
            'local_total_tva': instance.local_total_tva,
            'local_total_ttc': instance.local_total_ttc,
        }
        return self.render_preview(context)
