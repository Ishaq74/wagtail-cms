from django.core.management.base import BaseCommand
from wagtail.models import Page
from service.models import ServiceIndexPage, ServiceCategoryPage, ServicePage
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Populate the 'services' app with categories and services for Casa Nela"

    def handle(self, *args, **kwargs):
        self.populate_services()

    def get_homepage(self):
        """Retrieve the homepage."""
        homepage = Page.objects.filter(depth=2).first()
        if not homepage:
            self.stdout.write("Erreur : aucune page d'accueil trouvée. Configurez une page d'accueil avant d'exécuter ce script.")
        return homepage

    def create_service_index_page(self, homepage):
        """Create or retrieve the ServiceIndexPage."""
        if ServiceIndexPage.objects.exists():
            self.stdout.write("La page d'index des services existe déjà.")
            return ServiceIndexPage.objects.first()

        service_index = ServiceIndexPage(
            title="Nos Services",
            subtitle="Découvrez ce que nous offrons",
            summary="Une vue d'ensemble des services disponibles chez Casa Nela, adaptés à vos besoins.",
            live=True,
        )
        homepage.add_child(instance=service_index)
        service_index.save_revision().publish()
        self.stdout.write("Page d'index des services créée avec succès.")
        return service_index

    def create_service_category(self, index_page, title, subtitle="", summary="", featured_image=None):
        """Create or retrieve a ServiceCategoryPage."""
        category = ServiceCategoryPage.objects.filter(title=title, path__startswith=index_page.path).first()
        if category:
            self.stdout.write(f"La catégorie '{title}' existe déjà.")
            return category

        category = ServiceCategoryPage(
            title=title,
            subtitle=subtitle,
            summary=summary,
            featured_image=featured_image,
            live=True,
        )
        index_page.add_child(instance=category)
        category.save_revision().publish()
        self.stdout.write(f"Catégorie créée : {title}")
        return category

    def create_service_page(self, category_page, title, subtitle, summary, content, area_served, is_featured=False):
        """Create or retrieve a ServicePage."""
        slug = slugify(title)
        service = ServicePage.objects.filter(slug=slug, path__startswith=category_page.path).first()
        if service:
            self.stdout.write(f"Le service '{title}' existe déjà dans la catégorie '{category_page.title}'.")
            return service

        service = ServicePage(
            title=title,
            subtitle=subtitle,
            summary=summary,
            content=content,
            area_served=area_served,
            is_featured=is_featured,
            live=True,
        )
        category_page.add_child(instance=service)
        service.save_revision().publish()
        self.stdout.write(f"Service créé : {title}")
        return service

    def populate_services(self):
        """Populate the services app with categories and services."""
        homepage = self.get_homepage()
        if not homepage:
            return

        index_page = self.create_service_index_page(homepage)

        # Service categories
        categories = [
            {"title": "Commandes", "subtitle": "Commandes en ligne", "summary": "Commandez vos plats préférés rapidement et facilement."},
            {"title": "Livraison", "subtitle": "Livraison à domicile", "summary": "Recevez vos commandes directement chez vous."},
            {"title": "Événements", "subtitle": "Organisation d'événements", "summary": "Organisez vos réceptions et fêtes avec nous."},
        ]

        category_objects = {}
        for category_data in categories:
            category_objects[category_data["title"]] = self.create_service_category(
                index_page,
                title=category_data["title"],
                subtitle=category_data["subtitle"],
                summary=category_data["summary"],
            )

        # Services
        services = [
            # Commandes
            {
                "category": "Commandes",
                "title": "Commande en ligne",
                "subtitle": "Un service rapide et simple",
                "summary": "Commandez en ligne et récupérez votre commande directement au restaurant.",
                "content": "Utilisez notre plateforme de commande en ligne pour choisir vos plats préférés et les récupérer à l'heure qui vous convient.",
                "area_served": "Annecy et ses alentours",
                "is_featured": True,
            },
            {
                "category": "Commandes",
                "title": "Précommande pour événements",
                "subtitle": "Anticipez vos commandes",
                "summary": "Passez vos commandes à l'avance pour vos événements ou réunions.",
                "content": "Planifiez à l'avance vos commandes pour vos occasions spéciales.",
                "area_served": "Annecy et alentours",
            },
            # Livraison
            {
                "category": "Livraison",
                "title": "Livraison standard",
                "subtitle": "Recevez vos commandes à domicile",
                "summary": "Livraison rapide et fiable à domicile.",
                "content": "Nous livrons vos plats préférés directement chez vous en toute sécurité.",
                "area_served": "Annecy centre",
                "is_featured": True,
            },
            {
                "category": "Livraison",
                "title": "Livraison express",
                "subtitle": "Livraison en moins de 30 minutes",
                "summary": "Pour les commandes urgentes, choisissez notre option express.",
                "content": "Avec la livraison express, vos plats sont livrés chauds et rapidement.",
                "area_served": "Annecy, Seynod, Cran-Gevrier",
            },
            # Événements
            {
                "category": "Événements",
                "title": "Catering pour mariages",
                "subtitle": "Un service complet pour vos mariages",
                "summary": "Menus personnalisés et service dédié pour vos mariages.",
                "content": "Notre équipe prend en charge le catering pour faire de votre mariage un moment inoubliable.",
                "area_served": "Annecy et Haute-Savoie",
            },
            {
                "category": "Événements",
                "title": "Organisation d'anniversaires",
                "subtitle": "Fêtes réussies",
                "summary": "Organisez un anniversaire mémorable avec notre aide.",
                "content": "Nous fournissons les repas, boissons et services pour que vous profitiez de la fête.",
                "area_served": "Annecy et environs",
            },
        ]

        for service_data in services:
            category = category_objects.get(service_data["category"])
            if category:
                self.create_service_page(
                    category_page=category,
                    title=service_data["title"],
                    subtitle=service_data["subtitle"],
                    summary=service_data["summary"],
                    content=service_data["content"],
                    area_served=service_data["area_served"],
                    is_featured=service_data.get("is_featured", False),
                )

        self.stdout.write("Population de l'application 'services' terminée avec succès.")
