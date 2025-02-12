from django.core.management.base import BaseCommand
from wagtail.models import Page
from product.models import (
    ProductIndexPage, ProductCategory, ProductPage, ProductVariant, VariantOption
)
from decimal import Decimal, InvalidOperation


class Command(BaseCommand):
    help = "Populate the 'product' app with real data for Casa Nela"

    def handle(self, *args, **kwargs):
        self.populate_products()

    def get_homepage(self):
        """Retrieve the homepage, ensuring it exists."""
        homepage = Page.objects.filter(depth=2).first()
        if not homepage:
            self.stdout.write("Erreur : aucune page d'accueil trouvée. Configurez une page d'accueil avant d'exécuter ce script.")
        return homepage

    def create_product_index_page(self, homepage):
        """Create or retrieve the ProductIndexPage."""
        if ProductIndexPage.objects.exists():
            self.stdout.write("La page d'index des produits existe déjà.")
            return ProductIndexPage.objects.first()

        product_index = ProductIndexPage(
            title="Boutique",
            intro="Bienvenue sur notre boutique en ligne.",
            live=True,
        )
        homepage.add_child(instance=product_index)
        product_index.save_revision().publish()
        self.stdout.write("Page d'index des produits créée avec succès.")
        return product_index

    def create_product_category(self, index_page, title, summary="Catégorie de produits", is_featured=False):
        """Create or retrieve a ProductCategory."""
        category = ProductCategory.objects.filter(title=title, path__startswith=index_page.path).first()
        if category:
            self.stdout.write(f"La catégorie '{title}' existe déjà.")
            return category

        category = ProductCategory(
            title=title,
            summary=summary,
            is_featured=is_featured,
            live=True,
        )
        index_page.add_child(instance=category)
        category.save_revision().publish()
        self.stdout.write(f"Catégorie créée : {title}")
        return category

    def create_product(self, title, description, price, category_titles):
        """Create or retrieve a ProductPage and associate it with categories."""
        # Vérifie si le produit existe déjà
        product = ProductPage.objects.filter(title=title).first()
        try:
            price = round(Decimal(price), 2)
        except InvalidOperation:
            self.stdout.write(f"Erreur : Le prix '{price}' pour le produit '{title}' est invalide.")
            return

        # Associer le produit à une catégorie parent
        parent_category = None
        for category_title in category_titles:
            parent_category = ProductCategory.objects.filter(title=category_title).first()
            if parent_category:
                break

        if not parent_category:
            self.stdout.write(f"Erreur : Aucune catégorie valide trouvée pour le produit '{title}'.")
            return

        if product:
            self.stdout.write(f"Le produit '{title}' existe déjà dans '{parent_category.title}'. Mise à jour des catégories.")
        else:
            # Crée le produit comme enfant de la première catégorie trouvée
            product = ProductPage(
                title=title,
                summary=description,
                price=price,
                live=True,
            )
            parent_category.add_child(instance=product)
            product.save_revision().publish()
            self.stdout.write(f"Produit créé : {title} sous '{parent_category.title}'.")

        # Associe les catégories supplémentaires (Many-to-Many)
        for category_title in category_titles:
            category = ProductCategory.objects.filter(title=category_title).first()
            if category and category not in product.categories.all():
                product.categories.add(category)
                self.stdout.write(f"Ajouté à la catégorie : {category.title}")
        product.save()

    def create_product_variant(self, variant_name, options):
        """Create or retrieve a product variant."""
        variant, created = ProductVariant.objects.get_or_create(name=variant_name)
        if created:
            self.stdout.write(f"Variante créée : {variant_name}")

        for option_name, additional_price in options:
            VariantOption.objects.get_or_create(
                variant=variant,
                name=option_name,
                defaults={"additional_price": additional_price},
            )
        return variant

    def populate_products(self):
        """Execute the population of the product app."""
        homepage = self.get_homepage()
        if not homepage:
            return

        index_page = self.create_product_index_page(homepage)

        # Main categories
        categories = [
            "Menu Étudiant",
            "Pâtes",
            "Salades",
            "Autres Choix",
            "Boissons Chaudes",
            "Boissons Fraîches",
            "Gourmandises",
            "Milkshakes",
            "Smoothies",
        ]

        # Create categories
        category_objects = {}
        for title in categories:
            category_objects[title] = self.create_product_category(index_page, title)

        products = [
            # Menu Étudiant
            ("Napolitaine", "Tomates fraîches, basilic et huile d'olive", 7.90, ["Menu Étudiant"]),
            ("Pesto Vert ou Rouge", "Basilic, pignons de pin, parmesan", 7.90, ["Menu Étudiant"]),
            ("Fromagère", "Mozzarella, cheddar, parmesan, crème fraîche", 7.90, ["Menu Étudiant"]),
            ("Alfredo", "Poulet, champignons, crème fraîche", 9.90, ["Menu Étudiant"]),
            ("Bolognaise", "Bœuf haché, tomates, oignons", 9.90, ["Menu Étudiant"]),
            ("Saumon", "Saumon frais, ciboulette, mascarpone", 9.90, ["Menu Étudiant"]),
            ("Recette du jour", "Selon l’humeur de la cheffe !", 9.90, ["Menu Étudiant"]),

            # Pâtes
            ("Napolitaine", "Tomates fraîches, basilic et huile d'olive", 7.90, ["Pâtes"]),
            ("Pesto Vert ou Rouge", "Basilic, pignons de pin, parmesan", 7.90, ["Pâtes"]),
            ("Fromagère", "Mozzarella, cheddar, parmesan, crème fraîche", 7.90, ["Pâtes"]),
            ("Alfredo", "Poulet, champignons, crème fraîche", 9.90, ["Pâtes"]),
            ("Bolognaise", "Bœuf haché, tomates, oignons", 9.90, ["Pâtes"]),
            ("Saumon", "Saumon frais, ciboulette, mascarpone", 9.90, ["Pâtes"]),
            ("Recette du jour", "Selon l’humeur de la cheffe !", 9.90, ["Pâtes"]),

            # Salades
            ("Salade Casa", "Pâtes, saumon, tomates cerises, olives, mozzarella", 9.90, ["Salades"]),
            ("Salade Nela", "Poulet, parmesan, tomates cerises, olives", 9.90, ["Salades"]),
            ("Salade Burrata", "Tomates, burratina, pesto", 8.90, ["Salades"]),

            # Autres Choix
            ("Pizza Napolitaine", "Base tomate, mozzarella, basilic frais", 10.90, ["Autres Choix"]),
            ("Quiche Lorraine", "Lardons, crème fraîche, fromage", 8.50, ["Autres Choix"]),
            ("Croque Monsieur", "Pain de mie, jambon, fromage fondu", 6.50, ["Autres Choix"]),

            # Boissons Chaudes
            ("Ristretto", "Petit café intense", 1.80, ["Boissons Chaudes"]),
            ("Expresso", "Café classique", 1.80, ["Boissons Chaudes"]),
            ("Latte Macchiato", "Lait chaud et café", 3.80, ["Boissons Chaudes"]),
            ("Cappuccino", "Café avec mousse de lait", 3.50, ["Boissons Chaudes"]),
            ("Thé Vert", "Infusion chaude", 2.50, ["Boissons Chaudes"]),
            ("Chocolat Chaud", "Boisson chaude au chocolat", 3.00, ["Boissons Chaudes"]),

            # Boissons Fraîches
            ("Canette 33 CL", "Soda frais", 2.50, ["Boissons Fraîches"]),
            ("Jus de Fruits 25 CL", "Jus naturel", 3.50, ["Boissons Fraîches"]),
            ("Eau Minérale 50 CL", "Eau plate ou pétillante", 1.50, ["Boissons Fraîches"]),
            ("Diabolo Fraise", "Soda mélangé au sirop de fraise", 2.80, ["Boissons Fraîches"]),
            ("Limonade Maison", "Boisson citronnée fraîche", 3.00, ["Boissons Fraîches"]),
            ("Cocktail Tropical", "Mélange exotique sans alcool", 4.50, ["Boissons Fraîches"]),

            # Milkshakes
            ("Milkshake Fraise", "Milkshake classique à la fraise", 4.50, ["Milkshakes"]),
            ("Milkshake Chocolat", "Milkshake au chocolat fondant", 4.50, ["Milkshakes"]),
            ("Milkshake Vanille", "Milkshake à la vanille douce", 4.50, ["Milkshakes"]),
            ("Milkshake Mangue", "Milkshake tropical à la mangue", 5.00, ["Milkshakes"]),

            # Smoothies
            ("Smoothie Fraise-Banane", "Smoothie frais et naturel", 4.50, ["Smoothies"]),
            ("Smoothie Mangue-Ananas", "Saveurs tropicales", 4.50, ["Smoothies"]),
            ("Smoothie Kiwi", "Smoothie vitaminé", 4.50, ["Smoothies"]),
            ("Smoothie Pomme-Verte", "Smoothie acidulé", 4.50, ["Smoothies"]),

            # Gourmandises
            ("Tiramisu Maison", "Classique italien", 3.90, ["Gourmandises"]),
            ("Monte Bianco", "Dessert crémeux", 3.90, ["Gourmandises"]),
            ("Muffin au Chocolat", "Gâteau individuel au chocolat", 2.90, ["Gourmandises"]),
            ("Brownie", "Délicieux gâteau au chocolat et noix", 3.00, ["Gourmandises"]),
            ("Cookies", "Biscuits croquants", 1.50, ["Gourmandises"]),
            ("Macarons", "Douceur française", 4.00, ["Gourmandises"]),
            ("Crêpe Sucrée", "Garnie de sucre ou Nutella", 2.50, ["Gourmandises"]),
            ("Gaufre Maison", "Avec sucre glace ou chocolat", 3.00, ["Gourmandises"]),
        ]


        for title, description, price, categories in products:
            self.create_product(title, description, price, categories)

        # Variants
        self.create_product_variant("Type de pâtes", [
            ("Linguine", 0),
            ("Fuselloni", 0),
        ])
        self.create_product_variant("Fromages", [
            ("Parmigiano", 0),
            ("Mozzarella", 0),
            ("Burrata 100g", 3.00),
        ])

        self.stdout.write("Population de l'application 'product' terminée avec succès.")
