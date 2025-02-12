from django.core.management.base import BaseCommand
from wagtail.models import Page
from wagtail.images.models import Image
from blog.models import BlogIndexPage, BlogCategoryPage, BlogPage
from datetime import date
from django.utils.text import slugify



class Command(BaseCommand):
    help = "Populate the 'blog' app with complete data for a realistic scenario"

    def handle(self, *args, **kwargs):
        self.populate_blog()

    def get_homepage(self):
        """Retrieve the homepage, ensuring it exists."""
        homepage = Page.objects.filter(depth=2).first()
        if not homepage:
            self.stdout.write("Erreur : aucune page d'accueil trouvée. Configurez une page d'accueil avant d'exécuter ce script.")
        return homepage

    def create_blog_index_page(self, homepage):
        """Create or retrieve the BlogIndexPage."""
        if BlogIndexPage.objects.exists():
            self.stdout.write("La page d'accueil du blog existe déjà.")
            return BlogIndexPage.objects.first()

        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            excerpt="Bienvenue sur notre blog où nous partageons des articles inspirants.",
            content="<p>Découvrez nos dernières actualités et articles.</p>",
            live=True,
        )
        homepage.add_child(instance=blog_index)
        blog_index.save_revision().publish()
        self.stdout.write("Page d'accueil du blog créée avec succès.")
        return blog_index

    def create_blog_category(self, index_page, title, excerpt, content):
        """Create or retrieve a BlogCategoryPage."""
        category = BlogCategoryPage.objects.filter(title=title, path__startswith=index_page.path).first()
        if category:
            self.stdout.write(f"La catégorie '{title}' existe déjà.")
            return category

        category = BlogCategoryPage(
            title=title,
            slug=title.lower().replace(" ", "-"),
            excerpt=excerpt,
            content=content,
            live=True,
        )
        index_page.add_child(instance=category)
        category.save_revision().publish()
        self.stdout.write(f"Catégorie créée : {title}")
        return category

    def create_blog_article(self, category_page, title, date_published, excerpt, content, is_featured=False):
        """Create or retrieve a BlogPage under a category."""
        # Vérifie si la catégorie est valide et attachée à l'arbre
        if category_page.depth <= 1 or not category_page.path:
            self.stdout.write(f"Erreur : La catégorie '{category_page.title}' n'est pas correctement attachée à l'arbre.")
            return None

        # Génère un slug valide
        valid_slug = slugify(title)

        # Vérifie si l'article existe déjà
        article = BlogPage.objects.filter(slug=valid_slug, path__startswith=category_page.path).first()
        if article:
            self.stdout.write(f"L'article '{title}' existe déjà dans la catégorie '{category_page.title}'.")
            return article

        # Crée l'article
        article = BlogPage(
            title=title,
            slug=valid_slug,
            date=date_published,
            excerpt=excerpt,
            content=content,
            is_featured=is_featured,
            live=True,
        )

        # Ajoute l'article à la catégorie
        try:
            category_page.add_child(instance=article)
            article.save_revision().publish()
            self.stdout.write(f"Article créé : {title}")
        except Exception as e:
            self.stdout.write(f"Erreur lors de la création de l'article '{title}': {e}")
        return article

    def populate_blog(self):
        """Populate the blog with categories and articles."""
        homepage = self.get_homepage()
        if not homepage:
            return

        blog_index = self.create_blog_index_page(homepage)

        # Catégories de blog
        categories_data = [
            {
                "title": "Actualités",
                "excerpt": "Les dernières nouvelles de notre entreprise.",
                "content": "<p>Toutes nos actualités récentes.</p>",
            },
            {
                "title": "Recettes",
                "excerpt": "Des idées de recettes savoureuses pour toutes les occasions.",
                "content": "<p>Des recettes originales et faciles à réaliser.</p>",
            },
            {
                "title": "Conseils",
                "excerpt": "Des astuces pratiques pour améliorer votre quotidien.",
                "content": "<p>Des conseils pour mieux organiser votre vie.</p>",
            },
        ]

        categories = {}
        for category_data in categories_data:
            category = self.create_blog_category(
                blog_index,
                title=category_data["title"],
                excerpt=category_data["excerpt"],
                content=category_data["content"],
            )
            categories[category_data["title"]] = category

        # Articles
        articles_data = [
            {
                "title": "Lancement de notre nouveau service",
                "category": "Actualités",
                "date_published": date(2024, 1, 15),
                "excerpt": "Nous sommes ravis de vous présenter notre nouveau service.",
                "content": "<p>Découvrez les détails de notre nouvelle offre.</p>",
                "is_featured": True,
            },
            {
                "title": "Recette facile : Pâtes au pesto maison",
                "category": "Recettes",
                "date_published": date(2024, 2, 10),
                "excerpt": "Préparez un délicieux plat de pâtes au pesto maison.",
                "content": "<p>Une recette simple et rapide pour régaler toute la famille.</p>",
                "is_featured": False,
            },
            {
                "title": "10 astuces pour économiser de l'énergie",
                "category": "Conseils",
                "date_published": date(2024, 3, 5),
                "excerpt": "Découvrez comment réduire vos dépenses énergétiques.",
                "content": "<p>Des astuces simples et efficaces.</p>",
                "is_featured": False,
            },
        ]

        for article_data in articles_data:
            category_page = categories[article_data["category"]]
            self.create_blog_article(
                category_page=category_page,
                title=article_data["title"],
                date_published=article_data["date_published"],
                excerpt=article_data["excerpt"],
                content=article_data["content"],
                is_featured=article_data["is_featured"],
            )

        self.stdout.write("Population de l'application 'blog' terminée avec succès.")
