"""
Base classes and mixins for Wagtail streamfields.

This module provides the foundation for the EXTRAORDINARY streamfield system
with standardized patterns, reusable mixins, and consistent functionality.
"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class BaseStructBlock(blocks.StructBlock):
    """Enhanced base class for all custom struct blocks with common functionality."""
    
    def clean(self, value):
        """Enhanced validation for struct blocks."""
        cleaned_value = super().clean(value)
        self.validate_block_specific(cleaned_value)
        return cleaned_value
    
    def validate_block_specific(self, value):
        """Override in subclasses for block-specific validation."""
        pass
    
    def get_context(self, value, parent_context=None):
        """Enhanced context with common utilities."""
        context = super().get_context(value, parent_context)
        context.update({
            'block_id': self.get_block_id(value),
            'css_classes': self.get_css_classes(value),
            'data_attributes': self.get_data_attributes(value),
        })
        return context
    
    def get_block_id(self, value):
        """Generate unique block ID."""
        label = getattr(self.meta, 'label', None) or self.__class__.__name__
        return f"{label.lower().replace(' ', '-')}-{hash(str(value)) % 10000}"
    
    def get_css_classes(self, value):
        """Generate CSS classes based on block configuration."""
        classes = []
        
        # Ensure value is dict-like
        if not isinstance(value, dict):
            return ''
        
        # Add alignment classes
        if 'alignment' in value and value.get('alignment'):
            classes.append(f"text-{value['alignment']}")
        
        # Add color classes  
        if 'color' in value and value.get('color'):
            classes.append(f"text-{value['color']}")
            
        # Add spacing classes
        if 'spacing' in value and value.get('spacing'):
            classes.append(f"spacing-{value['spacing']}")
            
        return ' '.join(classes)
    
    def get_data_attributes(self, value):
        """Generate data attributes for enhanced functionality."""
        return {}


class DesignMixin(blocks.StructBlock):
    """Mixin providing design-related fields with design system integration."""
    
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('center', 'Center'),
            ('right', 'Right'),
            ('justify', 'Justify')
        ], 
        default='left', 
        help_text="Text alignment"
    )
    
    color = blocks.ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('accent', 'Accent'),
            ('neutral', 'Neutral'),
            ('base', 'Base'),
            ('info', 'Info'),
            ('success', 'Success'),
            ('warning', 'Warning'),
            ('error', 'Error')
        ], 
        default='base',
        help_text="Text color from design system"
    )
    
    spacing = blocks.ChoiceBlock(
        choices=[
            ('none', 'None'),
            ('xs', 'Extra Small'),
            ('sm', 'Small'),
            ('md', 'Medium'),
            ('lg', 'Large'),
            ('xl', 'Extra Large'),
            ('2xl', 'Double Extra Large')
        ], 
        default='md',
        help_text="Spacing around the element"
    )


class ResponsiveImageMixin(blocks.StructBlock):
    """Mixin for responsive images with modern best practices."""
    
    image = ImageChooserBlock(required=True, help_text="Choose an image")
    
    alt_text = blocks.CharBlock(
        required=False, 
        blank=True, 
        max_length=255, 
        help_text="Alternative text for accessibility (auto-generated if empty)"
    )
    
    sizes = blocks.ChoiceBlock(
        choices=[
            ('xs', 'Extra Small (max-width: 320px)'),
            ('sm', 'Small (max-width: 768px)'),
            ('md', 'Medium (max-width: 1024px)'),
            ('lg', 'Large (max-width: 1280px)'),
            ('xl', 'Extra Large (max-width: 1920px)'),
            ('full', 'Full Width'),
            ('auto', 'Auto Size')
        ],
        default='md',
        help_text="Image size and breakpoint behavior"
    )
    
    aspect_ratio = blocks.ChoiceBlock(
        choices=[
            ('auto', 'Auto'),
            ('square', '1:1 Square'),
            ('landscape', '4:3 Landscape'),
            ('portrait', '3:4 Portrait'),
            ('wide', '16:9 Wide'),
            ('ultra-wide', '21:9 Ultra Wide')
        ],
        default='auto',
        help_text="Aspect ratio constraint"
    )
    
    loading = blocks.ChoiceBlock(
        choices=[
            ('lazy', 'Lazy Loading (recommended)'),
            ('eager', 'Immediate Loading')
        ],
        default='lazy',
        help_text="Image loading behavior"
    )


class AccessibilityMixin(blocks.StructBlock):
    """Mixin for enhanced accessibility features."""
    
    aria_label = blocks.CharBlock(
        required=False,
        blank=True,
        max_length=100,
        help_text="ARIA label for screen readers"
    )
    
    tab_index = blocks.IntegerBlock(
        required=False,
        blank=True,
        help_text="Tab order (leave empty for default)"
    )


class AnimationMixin(blocks.StructBlock):
    """Mixin for animation and interaction effects."""
    
    animation = blocks.ChoiceBlock(
        choices=[
            ('none', 'No Animation'),
            ('fade-in', 'Fade In'),
            ('slide-up', 'Slide Up'),
            ('slide-down', 'Slide Down'),
            ('slide-left', 'Slide Left'),
            ('slide-right', 'Slide Right'),
            ('zoom-in', 'Zoom In'),
            ('bounce', 'Bounce')
        ],
        default='none',
        help_text="Animation effect when element comes into view"
    )
    
    animation_delay = blocks.ChoiceBlock(
        choices=[
            ('0', 'No Delay'),
            ('100', '100ms'),
            ('200', '200ms'),
            ('300', '300ms'),
            ('500', '500ms'),
            ('750', '750ms'),
            ('1000', '1s')
        ],
        default='0',
        help_text="Animation delay"
    )


class LinkMixin(blocks.StructBlock):
    """Enhanced mixin for link handling with better UX."""
    
    link = blocks.PageChooserBlock(
        required=False, 
        help_text="Internal page link"
    )
    
    external_url = blocks.URLBlock(
        required=False, 
        help_text="External URL (if no internal page selected)"
    )
    
    link_text = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text="Custom link text (override default)"
    )
    
    link_target = blocks.ChoiceBlock(
        choices=[
            ('_self', 'Same Window'),
            ('_blank', 'New Window'),
            ('_parent', 'Parent Frame'),
        ],
        default='_self',
        help_text="Where to open the link"
    )
    
    link_rel = blocks.ChoiceBlock(
        choices=[
            ('', 'Default'),
            ('nofollow', 'No Follow'),
            ('noopener', 'No Opener'),
            ('nofollow noopener', 'No Follow + No Opener'),
        ],
        default='',
        required=False,
        help_text="Link relationship attributes"
    )
    
    def get_link_url(self, value):
        """Get the final URL for the link."""
        if value.get('link'):
            return value['link'].url
        elif value.get('external_url'):
            return value['external_url']
        return '#'
    
    def get_link_attributes(self, value):
        """Get HTML attributes for the link."""
        attrs = {
            'href': self.get_link_url(value),
            'target': value.get('link_target', '_self'),
        }
        
        if value.get('link_rel'):
            attrs['rel'] = value['link_rel']
            
        if value.get('aria_label'):
            attrs['aria-label'] = value['aria_label']
            
        return attrs


class BaseContentBlock(BaseStructBlock, DesignMixin, AccessibilityMixin, AnimationMixin):
    """Base class for content blocks with all common mixins."""
    
    def get_css_classes(self, value):
        """Enhanced CSS class generation."""
        classes = super().get_css_classes(value)
        
        # Add animation classes
        if value.get('animation', 'none') != 'none':
            classes += f" animate-{value['animation']}"
            if value.get('animation_delay', '0') != '0':
                classes += f" animate-delay-{value['animation_delay']}"
        
        return classes.strip()


class BaseListBlock(BaseStructBlock):
    """Base class for content list blocks with pagination support."""
    
    def validate_block_specific(self, value):
        """Validate list-specific requirements."""
        limit = value.get('limit', 0)
        if limit <= 0:
            raise ValidationError("Limit must be greater than 0")
        if limit > 100:
            raise ValidationError("Limit cannot exceed 100 items")
    
    def get_queryset(self, value, model_class):
        """Get base queryset for the list - override in subclasses."""
        return model_class.objects.live()
    
    def apply_filters(self, queryset, value):
        """Apply filters to queryset - override in subclasses."""
        return queryset
    
    def get_context(self, value, parent_context=None):
        """Enhanced context with pagination support."""
        context = super().get_context(value, parent_context)
        request = parent_context.get('request') if parent_context else None
        
        # Get and filter queryset
        queryset = self.get_filtered_queryset(value)
        
        # Apply pagination if request available
        if request and value.get('paginated', False):
            paginator = Paginator(queryset, value.get('limit', 6))
            page_number = request.GET.get('page')
            
            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
                
            context['items'] = page_obj
            context['is_paginated'] = True
        else:
            # Simple limit without pagination
            limit = value.get('limit', 6)
            context['items'] = queryset[:limit]
            context['is_paginated'] = False
            
        return context
    
    def get_filtered_queryset(self, value):
        """Get queryset with all filters applied - implement in subclasses."""
        raise NotImplementedError("Subclasses must implement get_filtered_queryset")