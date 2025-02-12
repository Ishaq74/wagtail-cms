from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Currency(ClusterableModel):
    code = models.CharField(max_length=10, unique=True, verbose_name="Code de la devise")
    gain_exchange_rate = models.IntegerField(
        default=756,verbose_name="Taux de change (gain)"
    )
    lose_exchange_rate = models.IntegerField(
        default=656, verbose_name="Taux de change (perte)"
    )

    class Meta:
        verbose_name = "Devise"
        verbose_name_plural = "Devises"

    def __str__(self):
        return f"{self.code} (Gain: {self.gain_exchange_rate}, Perte: {self.lose_exchange_rate})"

    panels = [
        FieldPanel("code"),
        FieldPanel("gain_exchange_rate"),
        FieldPanel("lose_exchange_rate"),
        InlinePanel("rates", label="Historique des taux de change"),
    ]

class RateCurrency(models.Model):
    currency = ParentalKey(
        Currency, on_delete=models.CASCADE, related_name="rates", verbose_name="Devise"
    )
    date = models.DateField(verbose_name="Date du taux de change")
    rate = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Taux de change"
    )

    def __str__(self):
        return f"{self.currency.code} - {self.date}: {self.rate}"

    panels = [
        FieldPanel("date"),
        FieldPanel("rate"),
    ]
