# EXTRAORDINARY Wagtail CMS Design System & Streamfields

This document describes the comprehensive design system and streamfield architecture implemented for the Wagtail CMS project.

## Overview

The system provides:
- **Standardized streamfield blocks** with consistent patterns
- **Comprehensive design system** with design tokens
- **Modular architecture** reducing code duplication
- **Enhanced functionality** with accessibility and responsive design
- **Theme support** with light/dark mode variations

## Streamfield Architecture

### Base Classes

#### `BaseStructBlock`
Enhanced base class for all custom struct blocks with:
- Automatic block ID generation
- CSS class generation
- Data attributes management
- Enhanced validation

#### `BaseContentBlock`
Combines BaseStructBlock with common mixins:
- Design system integration (DesignMixin)
- Accessibility features (AccessibilityMixin)
- Animation support (AnimationMixin)

#### `BaseListBlock`
Specialized base for content list blocks with:
- Pagination support
- Filtering capabilities
- Validation for limits

### Mixins

#### `DesignMixin`
Provides design-related fields:
- `alignment`: Text alignment (left, center, right, justify)
- `color`: Color from design system palette
- `spacing`: Consistent spacing values

#### `ResponsiveImageMixin`
Modern image handling:
- `sizes`: Responsive breakpoint behavior
- `aspect_ratio`: Consistent aspect ratios
- `loading`: Lazy loading support
- `alt_text`: Accessibility text

#### `LinkMixin`
Enhanced link functionality:
- Internal page links
- External URLs
- Link targets and relationships
- Custom link text
- ARIA labels

#### `AccessibilityMixin`
Accessibility enhancements:
- ARIA labels
- Tab index management
- Screen reader support

#### `AnimationMixin`
Animation and interaction effects:
- Animation types (fade, slide, zoom, bounce)
- Animation delays
- Performance optimizations

### Enhanced Blocks

#### Content Blocks
- **HeadingBlock**: Enhanced headings with semantic levels and visual sizes
- **ParagraphBlock**: Rich text with lead paragraph option
- **ImageBlock**: Responsive images with modern features
- **QuoteBlock**: Styled quotes with attribution
- **EmbedBlock**: External content with aspect ratio control

#### Interactive Blocks
- **ButtonBlock**: Comprehensive button system with styles, sizes, and icons
- **ButtonGroupBlock**: Flexible button layouts
- **CallToActionBlock**: Complete CTA sections

#### Layout Blocks
- **ContainerBlock**: Flexible content containers
- **ColumnBlock**: Multi-column layouts (2-4 columns)
- **HeroBlock**: Landing page hero sections
- **AccordionBlock**: FAQ/expandable content

#### List Blocks
Configuration-driven blocks for different content types:
- **ProductListBlock**: Product listings with filtering
- **BlogListBlock**: Blog post listings
- **ServiceListBlock**: Service listings
- **BusinessListBlock**: Business listings

All list blocks support:
- Grid, list, card, and minimal layouts
- Responsive column control
- Featured item filtering
- Category filtering
- Pagination options

### Usage Examples

#### Basic Content Block
```python
# Using enhanced heading
heading = HeadingBlock()

# Value structure
{
    'heading_text': 'Welcome to Our Site',
    'heading_level': 'h1',
    'size': '3xl',
    'font_weight': 'bold',
    'alignment': 'center',
    'color': 'primary',
    'spacing': 'lg',
    'animation': 'fade-in',
    'animation_delay': '200'
}
```

#### Configuration-driven List
```python
# Product list with filtering
products = ProductListBlock()

# Value structure
{
    'heading': {
        'heading_text': 'Featured Products',
        'heading_level': 'h2'
    },
    'limit': 6,
    'layout': 'grid',
    'columns': 'auto',
    'featured_only': True,
    'categories': [category1, category2],
    'show_pagination': True
}
```

## Design System

### Design Tokens

The design system uses CSS custom properties for consistent theming:

#### Colors
```css
/* Primary brand colors */
--color-primary-50 to --color-primary-950

/* Secondary colors */
--color-secondary-50 to --color-secondary-950

/* Semantic colors */
--color-success, --color-warning, --color-error, --color-info

/* Neutral colors */
--color-neutral-50 to --color-neutral-950
```

#### Typography
```css
/* Font families */
--font-family-sans: 'Inter', ...
--font-family-serif: 'Playfair Display', ...
--font-family-mono: 'JetBrains Mono', ...

/* Responsive font sizes */
text-xs to text-9xl with proper line heights
```

#### Spacing
```css
/* Consistent spacing scale */
--spacing-xs: 0.5rem (8px)
--spacing-sm: 1rem (16px)
--spacing-md: 1.5rem (24px)
--spacing-lg: 2rem (32px)
--spacing-xl: 3rem (48px)
--spacing-2xl: 4rem (64px)
```

#### Shadows & Effects
```css
/* Elevation system */
--shadow-xs to --shadow-xl
--shadow-glow, --shadow-glow-lg

/* Border radius */
--radius-xs to --radius-2xl, --radius-full
```

### Component Classes

#### Buttons
```css
.btn - Base button class
.btn-xs, .btn-sm, .btn-md, .btn-lg, .btn-xl - Sizes
.btn-primary, .btn-secondary, .btn-accent - Colors
.btn-outline, .btn-ghost, .btn-link - Variants
```

#### Cards
```css
.card - Base card
.card-body, .card-header, .card-footer - Card sections
.card-interactive - Hover effects
```

#### Typography
```css
.heading-xs to .heading-6xl - Heading sizes
.lead - Lead paragraph style
.prose-enhanced - Enhanced prose styling
```

#### Layout
```css
.container-narrow, .container-standard, .container-wide - Containers
.section, .section-sm, .section-lg - Section spacing
.grid-cols-auto, .grid-cols-auto-sm, .grid-cols-auto-lg - Responsive grids
```

### Responsive Design

The system uses a mobile-first approach with breakpoints:
- `sm`: 640px
- `md`: 768px  
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

### Dark Mode Support

Full dark mode support with:
- Automatic color scheme switching
- CSS custom property overrides
- Consistent contrast ratios
- User preference detection

### Animation System

Performance-optimized animations:
- Fade, slide, zoom, and bounce effects
- Configurable delays
- Reduced motion support
- Hardware acceleration

## Migration Guide

### From Original Blocks

The enhanced system maintains backward compatibility:

1. **Template Compatibility**: Original template paths still work
2. **Data Preservation**: Existing content is preserved
3. **Gradual Migration**: Switch to new blocks progressively

### Migration Steps

1. **Replace Imports**:
```python
# Old
from streams.blocks import HeadingBlock

# New
from streams.enhanced_blocks import HeadingBlock
```

2. **Update Templates**: Use enhanced templates for new features
3. **Apply Design System**: Add design system classes gradually
4. **Test Functionality**: Ensure all features work as expected

## Performance Considerations

### CSS Optimization
- Purged unused classes in production
- Minimal CSS output (~100KB compressed)
- Modern CSS features with fallbacks
- Critical CSS inlining support

### Image Optimization
- Responsive image generation
- Lazy loading by default
- WebP format support
- Aspect ratio preservation

### JavaScript Minimal
- Pure CSS animations where possible
- Progressive enhancement
- No heavy framework dependencies

## Accessibility Features

### WCAG 2.1 AA Compliance
- Proper heading hierarchy
- Color contrast ratios
- Keyboard navigation
- Screen reader support
- Focus management

### Semantic HTML
- Proper element usage
- ARIA labels and roles
- Landmark regions
- Skip navigation links

## Browser Support

### Modern Browsers
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Graceful Degradation
- CSS Grid with Flexbox fallback
- Custom properties with fallback values
- Modern features with polyfills

## Development Workflow

### CSS Development
```bash
# Watch mode
npm run dev

# Production build
npm run build

# Linting
npm run lint
```

### Testing
```bash
# Run streamfield tests
python manage.py test streams.test_enhanced

# Run all tests
python manage.py test
```

### Deployment
1. Build CSS: `npm run build`
2. Collect static files: `python manage.py collectstatic`
3. Run migrations: `python manage.py migrate`

## Future Enhancements

### Phase 2 Features
- Advanced animation library
- Component documentation site
- Visual page builder integration
- Performance monitoring

### Phase 3 Features
- Multi-brand theme support
- Advanced typography system
- Micro-interactions library
- Design system governance

---

This design system provides the foundation for an **EXTRAORDINARY** Wagtail CMS experience with modern development practices, excellent performance, and outstanding user experience.