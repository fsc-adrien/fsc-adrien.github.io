#!/usr/bin/env python3
"""
FSC Blog Builder - Compile blogs using Handlebars-like template system

This script:
1. Reads all blog-*.html files
2. Extracts metadata (title, description, keywords, date, tags, content)
3. Loads template files from templates/ directory
4. Compiles and generates production-ready blog files
5. Ensures SEO optimization with canonical URLs, OG tags, Twitter cards

Features:
- Clean code architecture
- SEO-optimized output
- Consistent styling across all 78 blog files
- Single source of truth for header/footer
- Easy to maintain and extend
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

BLOG_DIR = Path(__file__).parent
TEMPLATE_DIR = BLOG_DIR / 'templates'
OUTPUT_DIR = BLOG_DIR

# Template files
TEMPLATE_LAYOUT = TEMPLATE_DIR / 'layout.hbs'
TEMPLATE_HEADER = TEMPLATE_DIR / '_header.hbs'
TEMPLATE_FOOTER = TEMPLATE_DIR / '_footer.hbs'
TEMPLATE_PAGE_HEADER = TEMPLATE_DIR / '_page-header.hbs'
TEMPLATE_BLOG_CONTENT = TEMPLATE_DIR / '_blog-content.hbs'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_between(html, start_tag, end_tag):
    """Extract text between HTML tags"""
    start_idx = html.find(start_tag)
    if start_idx == -1:
        return ''
    
    content_start = start_idx + len(start_tag)
    end_idx = html.find(end_tag, content_start)
    if end_idx == -1:
        return ''
    
    return html[content_start:end_idx].strip()

def extract_title(html):
    """Extract title from <title> tag"""
    match = re.search(r'<title>([^<]+)<\/title>', html, re.IGNORECASE)
    if match:
        title = match.group(1)
        title = re.sub(r'\s*-\s*FSC\s+Software\s+Blog', '', title, flags=re.IGNORECASE)
        return title.strip()
    return 'Blog Post'

def extract_meta_content(html, name):
    """Extract meta tag content by name or property"""
    pattern = f'<meta\\s+(?:name|property)=["\']?{name}["\']?\\s+content=["\']([^"\']+)["\']'
    match = re.search(pattern, html, re.IGNORECASE)
    return match.group(1) if match else ''

def extract_description(html):
    """Extract meta description"""
    desc = extract_meta_content(html, 'description')
    return desc if desc else 'Read our latest tech blog post'

def extract_keywords(html):
    """Extract meta keywords"""
    keywords = extract_meta_content(html, 'keywords')
    return keywords if keywords else 'blog, technology, software'

def extract_breadcrumb(title):
    """Create breadcrumb from title (first 40 chars)"""
    return title[:40] + '...' if len(title) > 40 else title

def extract_date(html):
    """Extract publish date from post-meta"""
    match = re.search(r'<div\s+class=["\']post-meta["\']>[\s\S]*?<span>([A-Za-z]+\s+\d+,\s+\d{4})', html)
    if match:
        return match.group(1)
    return datetime.now().strftime('%B %d, %Y')

def extract_tags(html):
    """Extract post tags"""
    match = re.search(r'<div\s+class=["\']post-tags["\']>([\s\S]*?)<\/div>', html)
    if not match:
        return []
    
    tags_html = match.group(1)
    tags = []
    
    for tag_match in re.finditer(r'<a[^>]*>([^<]+)<\/a>', tags_html):
        tag = tag_match.group(1).strip()
        if tag and tag != '#':
            tags.append(tag)
    
    return tags

def extract_content(html):
    """Extract blog content from post-content div"""
    # Find post-content section
    match = re.search(
        r'<div\s+class=["\']post-content["\']>([\s\S]*?)<\/div>\s*<div\s+class=["\']post-tags["\']',
        html
    )
    
    if not match:
        return '<p>Content not found</p>'
    
    content = match.group(1).strip()
    
    # Remove sidebar references
    content = re.sub(r'<div\s+class=["\']col-lg-\d+["\'][^>]*>[\s\S]*?<\/div>', '', content)
    
    # Remove aside tags
    content = re.sub(r'<aside[^>]*>[\s\S]*?<\/aside>', '', content)
    
    # Remove icon spans from styling (keep text)
    content = re.sub(r'<span><i\s+class=["\']fa[^"\']*["\'][^>]*><\/i>\s*', '<span>', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n', '\n', content)
    
    return content.strip()

def get_filename(filepath):
    """Get filename from path"""
    return os.path.basename(filepath)

# ============================================================================
# TEMPLATE FUNCTIONS
# ============================================================================

def load_template(template_path):
    """Load Handlebars template file"""
    if not template_path.exists():
        print(f'⚠️  Template not found: {template_path}')
        return ''
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def render_partial(template_content, partial_name, partial_content):
    """Replace {{> partial-name}} with partial content"""
    pattern = f'{{{{>\\s*{partial_name}\\s*}}}}'
    return re.sub(pattern, partial_content, template_content)

def render_variable(template_content, var_name, var_value):
    """Replace {{variable}} with value"""
    if isinstance(var_value, list):
        # For arrays, handle each item
        items_html = ''
        for item in var_value:
            items_html += f'<span class="tag">{item}</span>\n'
        pattern = f'{{{{#each\\s+{var_name}\\s*}}}}([\s\S]*?){{{{/each}}}}'
        replacement = items_html
        template_content = re.sub(pattern, replacement, template_content)
    else:
        # For strings, escape HTML
        value_str = str(var_value) if var_value is not None else ''
        value_str = value_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        pattern = f'{{{{{var_name}}}}}'
        template_content = template_content.replace(pattern, value_str)
        pattern_each = f'{{{{{{#if\\s+{var_name}\\s*}}}}}([\s\S]*?){{{{{{/if}}}}}}'
        if value_str:
            template_content = re.sub(pattern_each, r'\1', template_content)
    
    return template_content

def render_html_variable(template_content, var_name, var_value):
    """Replace {{{variable}}} with value (for HTML content, no escaping)"""
    pattern = f'{{{{{{{var_name}}}}}}}'
    template_content = template_content.replace(pattern, str(var_value) if var_value else '')
    return template_content

def compile_template(layout_content, partials, variables):
    """
    Compile Handlebars template with partials and variables
    
    partials: dict of {'partial-name': 'content'}
    variables: dict of {'var_name': value}
    """
    output = layout_content
    
    # 1. Replace partials first
    for partial_name, partial_content in partials.items():
        output = render_partial(output, partial_name, partial_content)
    
    # 2. Replace HTML variables (must be before regular variables)
    for var_name, var_value in variables.items():
        if var_name == 'content':  # HTML content without escaping
            output = render_html_variable(output, var_name, var_value)
    
    # 3. Replace regular variables
    for var_name, var_value in variables.items():
        if var_name != 'content':  # Skip HTML content
            output = render_variable(output, var_name, var_value)
    
    return output

# ============================================================================
# BUILD FUNCTIONS
# ============================================================================

def build_blog(filename):
    """Build a single blog file"""
    try:
        filepath = BLOG_DIR / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Extract metadata
        title = extract_title(html)
        description = extract_description(html)
        keywords = extract_keywords(html)
        breadcrumb = extract_breadcrumb(title)
        date = extract_date(html)
        tags = extract_tags(html)
        content = extract_content(html)
        filename_only = get_filename(filename)
        
        # Load templates
        layout = load_template(TEMPLATE_LAYOUT)
        if not layout:
            print(f'❌ Failed to load layout template')
            return False
        
        header = load_template(TEMPLATE_HEADER)
        footer = load_template(TEMPLATE_FOOTER)
        page_header = load_template(TEMPLATE_PAGE_HEADER)
        blog_content = load_template(TEMPLATE_BLOG_CONTENT)
        
        # Compile
        partials = {
            '_header': header,
            '_footer': footer,
            '_page-header': page_header,
            '_blog-content': blog_content
        }
        
        variables = {
            'title': title,
            'description': description,
            'keywords': keywords,
            'breadcrumb': breadcrumb,
            'date': date,
            'tags': tags,
            'content': content,
            'filename': filename_only
        }
        
        output = compile_template(layout, partials, variables)
        
        # Write output
        output_path = OUTPUT_DIR / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f'✅ Built: {filename}')
        return True
        
    except Exception as e:
        print(f'❌ Error building {filename}: {str(e)}')
        return False

def main():
    """Main build process"""
    print('📦 FSC Blog Builder - Starting...\n')
    
    # Find all blog files
    blog_files = sorted([
        f.name for f in BLOG_DIR.glob('blog-*.html')
    ])
    
    if not blog_files:
        print('⚠️  No blog files found in current directory')
        return
    
    print(f'📁 Found {len(blog_files)} blog files to process\n')
    
    # Build all blogs
    success_count = 0
    failure_count = 0
    
    for filename in blog_files:
        if build_blog(filename):
            success_count += 1
        else:
            failure_count += 1
    
    # Summary
    print(f'\n📊 Build Summary:')
    print(f'✅ Success: {success_count} files')
    print(f'❌ Failures: {failure_count} files')
    print(f'📁 Total: {len(blog_files)} files')
    
    if failure_count == 0:
        print('\n🎉 Build completed successfully!')
        return 0
    else:
        print('\n⚠️ Build completed with errors')
        return 1

if __name__ == '__main__':
    sys.exit(main())
