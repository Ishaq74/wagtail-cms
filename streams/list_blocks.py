"""
Configuration-driven list blocks to eliminate duplication.

This module provides a flexible system for creating list blocks for different
content types (products, blog posts, services, etc.) without code duplication.
"""

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail import blocks
from .base import BaseListBlock, BaseContentBlock
from .enhanced_blocks import HeadingBlock, ParagraphBlock


class ConfigurableListBlock(BaseListBlock):
    """Base configurable list block that can be adapted for any content type."""
    
    # Override these in subclasses
    MODEL_CLASS = None
    TEMPLATE_PREFIX = None
    CATEGORY_MODEL = None
    CATEGORY_FIELD = 'categories'
    
    heading = HeadingBlock(
        required=False, 
        help_text="Optional section heading"
    )
    
    description = ParagraphBlock(
        required=False,
        help_text="Optional section description"
    )
    
    limit = blocks.IntegerBlock(
        default=6,
        min_value=1,
        max_value=50,
        help_text="Number of items to display"
    )
    
    layout = blocks.ChoiceBlock(
        choices=[
            ('grid', 'Grid Layout'),
            ('list', 'List Layout'),
            ('cards', 'Card Layout'),
            ('minimal', 'Minimal Layout')
        ],
        default='grid',
        help_text="Layout style for items"
    )
    
    columns = blocks.ChoiceBlock(
        choices=[
            ('1', '1 Column'),
            ('2', '2 Columns'),
            ('3', '3 Columns'),
            ('4', '4 Columns'),
            ('auto', 'Auto (responsive)')
        ],
        default='auto',
        help_text="Number of columns (for grid layout)"
    )
    
    show_pagination = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="Enable pagination for large lists"
    )
    
    featured_only = blocks.BooleanBlock(
        required=False,
        help_text="Show only featured items"
    )
    
    def __init__(self, model_class=None, template_prefix=None, category_model=None, **kwargs):
        """Initialize with model configuration."""
        if model_class:
            self.MODEL_CLASS = model_class
        if template_prefix:
            self.TEMPLATE_PREFIX = template_prefix
        if category_model:
            self.CATEGORY_MODEL = category_model
        super().__init__(**kwargs)
    
    def get_filtered_queryset(self, value):
        """Get queryset with all filters applied."""
        if not self.MODEL_CLASS:
            raise ValueError("MODEL_CLASS must be set")
        
        queryset = self.MODEL_CLASS.objects.live().order_by('-first_published_at')
        
        # Apply featured filter
        if value.get('featured_only') and hasattr(self.MODEL_CLASS, 'is_featured'):
            queryset = queryset.filter(is_featured=True)
        
        # Apply category filters
        categories = value.get('categories')
        if categories and hasattr(self.MODEL_CLASS, self.CATEGORY_FIELD):
            queryset = queryset.filter(**{f"{self.CATEGORY_FIELD}__in": categories})
        
        return queryset.distinct()
    
    def get_context(self, value, parent_context=None):
        """Enhanced context with layout and styling information."""
        context = super().get_context(value, parent_context)
        
        context.update({
            'layout': value.get('layout', 'grid'),
            'columns': value.get('columns', 'auto'),
            'show_pagination': value.get('show_pagination', False),
            'heading': value.get('heading'),
            'description': value.get('description'),
        })
        
        return context
    
    @property
    def template_name(self):
        """Dynamic template name based on configuration."""
        if self.TEMPLATE_PREFIX:
            return f"{self.TEMPLATE_PREFIX}/configurable_list.html"
        return "streams/enhanced/configurable_list.html"
    
    class Meta:
        abstract = True


class CategoryFilterMixin(blocks.StructBlock):
    """Mixin to add category filtering to list blocks."""
    
    def __init__(self, category_model=None, **kwargs):
        self.category_model = category_model
        super().__init__(**kwargs)
        
        if category_model:
            # Add categories field dynamically
            self.child_blocks['categories'] = blocks.ListBlock(
                blocks.PageChooserBlock(target_model=category_model),
                required=False,
                help_text="Filter by categories (optional)"
            )


def create_list_block(model_class, template_prefix, category_model=None, 
                     additional_fields=None, meta_options=None):
    """Factory function to create configured list blocks."""
    
    # Base fields for all list blocks
    base_fields = {
        'heading': HeadingBlock(required=False, help_text="Optional section heading"),
        'description': ParagraphBlock(required=False, help_text="Optional section description"),
        'limit': blocks.IntegerBlock(
            default=6, min_value=1, max_value=50,
            help_text="Number of items to display"
        ),
        'layout': blocks.ChoiceBlock(
            choices=[
                ('grid', 'Grid Layout'),
                ('list', 'List Layout'), 
                ('cards', 'Card Layout'),
                ('minimal', 'Minimal Layout')
            ],
            default='grid',
            help_text="Layout style"
        ),
        'columns': blocks.ChoiceBlock(
            choices=[
                ('1', '1 Column'),
                ('2', '2 Columns'),
                ('3', '3 Columns'), 
                ('4', '4 Columns'),
                ('auto', 'Auto (responsive)')
            ],
            default='auto',
            help_text="Columns (for grid layout)"
        ),
        'show_pagination': blocks.BooleanBlock(
            required=False, default=False,
            help_text="Enable pagination"
        ),
        'featured_only': blocks.BooleanBlock(
            required=False,
            help_text="Show only featured items"
        ),
    }
    
    # Add category filtering if category model provided
    if category_model:
        base_fields['categories'] = blocks.ListBlock(
            blocks.PageChooserBlock(target_model=category_model),
            required=False,
            help_text="Filter by categories (optional)"
        )
    
    # Add any additional fields
    if additional_fields:
        base_fields.update(additional_fields)
    
    # Create the block class
    class DynamicListBlock(BaseListBlock):
        MODEL_CLASS = model_class
        TEMPLATE_PREFIX = template_prefix
        CATEGORY_MODEL = category_model
        
        def __init__(self, **kwargs):
            # Add fields to the block
            for field_name, field in base_fields.items():
                self.child_blocks[field_name] = field
            super().__init__(**kwargs)
        
        def get_filtered_queryset(self, value):
            """Get filtered queryset."""
            queryset = self.MODEL_CLASS.objects.live().order_by('-first_published_at')
            
            # Featured filter
            if value.get('featured_only') and hasattr(self.MODEL_CLASS, 'is_featured'):
                queryset = queryset.filter(is_featured=True)
            
            # Category filter  
            categories = value.get('categories')
            if categories and self.CATEGORY_MODEL:
                queryset = queryset.filter(categories__in=categories)
            
            return queryset.distinct()
    
    # Create Meta class dynamically after class definition
    meta_dict = {
        'template': f"{template_prefix}/configurable_list.html"
    }
    if meta_options:
        meta_dict.update(meta_options)
    
    DynamicListBlock.Meta = type('Meta', (), meta_dict)
    
    return DynamicListBlock


# Pre-configured blocks for common content types

def ProductListBlock():
    """Product list block factory."""
    try:
        from product.models import ProductPage, ProductCategory
        return create_list_block(
            model_class=ProductPage,
            template_prefix="product",
            category_model=ProductCategory,
            meta_options={
                'icon': 'tag',
                'label': 'Product List'
            }
        )()
    except ImportError:
        # Fallback if product app not available
        return ConfigurableListBlock()


def BlogListBlock():
    """Blog list block factory."""
    try:
        from blog.models import BlogPage, BlogCategoryPage
        return create_list_block(
            model_class=BlogPage,
            template_prefix="blog", 
            category_model=BlogCategoryPage,
            meta_options={
                'icon': 'doc-full',
                'label': 'Blog List'
            }
        )()
    except ImportError:
        return ConfigurableListBlock()


def ServiceListBlock():
    """Service list block factory."""
    try:
        from service.models import ServicePage, ServiceCategoryPage
        return create_list_block(
            model_class=ServicePage,
            template_prefix="service",
            category_model=ServiceCategoryPage, 
            meta_options={
                'icon': 'cogs',
                'label': 'Service List'
            }
        )()
    except ImportError:
        return ConfigurableListBlock()


def BusinessListBlock():
    """Business list block factory."""
    try:
        from businesslocal.models import BusinessLocalPage, BusinessLocalCategory
        return create_list_block(
            model_class=BusinessLocalPage,
            template_prefix="businesslocal",
            category_model=BusinessLocalCategory,
            meta_options={
                'icon': 'home',
                'label': 'Business List'
            }
        )()
    except ImportError:
        return ConfigurableListBlock()


# Category List Blocks

def CategoryListBlock(model_class, template_prefix, meta_options=None):
    """Generic category list block factory."""
    
    class DynamicCategoryListBlock(BaseListBlock):
        MODEL_CLASS = model_class
        TEMPLATE_PREFIX = template_prefix
        
        heading = HeadingBlock(required=False, help_text="Optional section heading")
        description = ParagraphBlock(required=False, help_text="Optional section description")
        limit = blocks.IntegerBlock(default=6, min_value=1, max_value=50)
        layout = blocks.ChoiceBlock(
            choices=[
                ('grid', 'Grid Layout'),
                ('list', 'List Layout'),
                ('cards', 'Card Layout')
            ],
            default='grid'
        )
        featured_only = blocks.BooleanBlock(required=False)
        show_pagination = blocks.BooleanBlock(required=False, default=False)
        
        def get_filtered_queryset(self, value):
            queryset = self.MODEL_CLASS.objects.live().order_by('title')
            
            if value.get('featured_only') and hasattr(self.MODEL_CLASS, 'is_featured'):
                queryset = queryset.filter(is_featured=True)
                
            return queryset.distinct()
    
    # Create Meta class dynamically after class definition
    meta_dict = {
        'template': f"{template_prefix}/category_list.html"
    }
    if meta_options:
        meta_dict.update(meta_options)
    
    DynamicCategoryListBlock.Meta = type('Meta', (), meta_dict)
    
    return DynamicCategoryListBlock


def ProductCategoryListBlock():
    """Product category list block."""
    try:
        from product.models import ProductCategory
        return CategoryListBlock(
            model_class=ProductCategory,
            template_prefix="product",
            meta_options={'icon': 'list-ul', 'label': 'Product Categories'}
        )()
    except ImportError:
        return ConfigurableListBlock()


def BlogCategoryListBlock():
    """Blog category list block."""
    try:
        from blog.models import BlogCategoryPage
        return CategoryListBlock(
            model_class=BlogCategoryPage,
            template_prefix="blog",
            meta_options={'icon': 'list-ul', 'label': 'Blog Categories'}
        )()
    except ImportError:
        return ConfigurableListBlock()


def ServiceCategoryListBlock():
    """Service category list block."""
    try:
        from service.models import ServiceCategoryPage
        return CategoryListBlock(
            model_class=ServiceCategoryPage,
            template_prefix="service", 
            meta_options={'icon': 'list-ul', 'label': 'Service Categories'}
        )()
    except ImportError:
        return ConfigurableListBlock()


def BusinessCategoryListBlock():
    """Business category list block.""" 
    try:
        from businesslocal.models import BusinessLocalCategory
        return CategoryListBlock(
            model_class=BusinessLocalCategory,
            template_prefix="businesslocal",
            meta_options={'icon': 'list-ul', 'label': 'Business Categories'}
        )()
    except ImportError:
        return ConfigurableListBlock()