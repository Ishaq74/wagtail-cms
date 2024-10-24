from wagtail import blocks
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class PaginatedServiceListBlock(blocks.StructBlock):
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de services à afficher par page")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        # Vérification de la présence du parent_context
        if parent_context is None:
            context['error'] = "Le contexte parent est manquant dans PaginatedServiceListBlock."
            context['services'] = []
            return context

        # Vérification de la présence de 'request' et 'page'
        request = parent_context.get('request')
        current_page = parent_context.get('page')

        # Cas où il manque request ou page
        if not request or not current_page:
            context['error'] = "Le contexte parent ne contient pas 'request' ou 'page'."
            context['services'] = []
            return context

        # On essaie de récupérer les services associés
        from .models import ServicePage
        services = ServicePage.objects.live().order_by('-first_published_at')  # Pas de descendant_of

        # Pagination
        paginator = Paginator(services, value['limit'])
        page_number = request.GET.get('page')

        try:
            services_paginated = paginator.page(page_number)
        except PageNotAnInteger:
            services_paginated = paginator.page(1)
        except EmptyPage:
            services_paginated = paginator.page(paginator.num_pages)

        context['services'] = services_paginated
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Liste de services avec pagination'
        template = 'streams/paginated_service_list.html'


class LimitedServiceListBlock(blocks.StructBlock):
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de services à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les services mis en avant")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        if parent_context is None:
            context['error'] = "Le contexte parent est manquant dans LimitedServiceListBlock."
            context['services'] = []
            return context

        from .models import ServicePage
        services = ServicePage.objects.live()

        if value['featured_only']:
            services = services.filter(is_featured=True)

        # Limiter le nombre de services renvoyés à la limite définie
        services = services.distinct()[:value['limit']]
        context['services'] = services
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste limitée de services'
        template = 'streams/limited_service_list.html'


class SiblingsServiceListBlock(blocks.StructBlock):
    limit = blocks.IntegerBlock(default=3, help_text="Nombre de services similaires à afficher")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        # Vérification que le parent_context est présent
        if parent_context is None:
            context['error'] = "Le contexte parent est manquant dans SiblingsServiceListBlock."
            context['siblings_services'] = []
            return context

        current_page = parent_context.get('page')
        if not current_page:
            context['error'] = "Impossible de récupérer la page actuelle pour les services similaires."
            context['siblings_services'] = []
            return context

        # Utiliser la méthode get_siblings_services() de la page pour obtenir les siblings
        siblings_services = current_page.get_siblings_services(limit=value['limit'])
        context['siblings_services'] = siblings_services
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Liste des services similaires'
        template = 'streams/siblings_service_list.html'
