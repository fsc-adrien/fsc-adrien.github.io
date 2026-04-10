#!/usr/bin/env python3
"""
Standardize and clean all blog HTML files
- Add proper head section with all meta tags, CSS, and SEO tags
- Format HTML properly (not minified)
- Ensure consistent structure
"""

import os
import re
from pathlib import Path

PROPER_HEAD_TEMPLATE = '''<!doctype html>
<html lang="en">

<head>
  <!-- META TAGS - SEO CRITICAL -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="author" content="FSC Software">
  <meta name="description" content="Read our latest tech blog post">
  <meta name="keywords" content="blog, technology, software">
  
  <!-- PAGE TITLE - SEO Critical -->
  <title>{TITLE}</title>

  <!-- OPEN GRAPH TAGS - Social Media Sharing -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="Read our latest tech blog post">
  <meta property="og:image" content="https://fsc-software.com/ico/preview.png">
  <meta property="og:site_name" content="FSC Software Blog">
  <meta property="og:url" content="https://fsc-software.com/{FILENAME}">

  <!-- TWITTER CARD TAGS - Twitter Sharing -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@fsc-software">
  <meta name="twitter:title" content="{TITLE}">
  <meta name="twitter:description" content="Read our latest tech blog post">
  <meta name="twitter:image" content="https://fsc-software.com/ico/preview.png">

  <!-- CANONICAL URL - Avoid duplicate content issues -->
  <link rel="canonical" href="https://fsc-software.com/{FILENAME}">

  <!-- FAVICON FILES - All sizes for various devices -->
  <link href="ico/favicon_fsc_144.png" rel="apple-touch-icon" sizes="144x144">
  <link href="ico/favicon_fsc_114.png" rel="apple-touch-icon" sizes="114x114">
  <link href="ico/favicon_fsc_72.png" rel="apple-touch-icon" sizes="72x72">
  <link href="ico/favicon_fsc_57.png" rel="apple-touch-icon">
  <link href="ico/favicon_fsc.png" rel="shortcut icon">

  <!-- CSS FILES - Stylesheets -->
  <link rel="stylesheet" href="css/animate.min.css">
  <link rel="stylesheet" href="css/font-awesome.min.css">
  <link rel="stylesheet" href="css/flipbox.min.css">
  <link rel="stylesheet" href="css/timeline.css">
  <link rel="stylesheet" href="css/odometer.min.css">
  <link rel="stylesheet" href="css/fancybox.min.css">
  <link rel="stylesheet" href="css/swiper.min.css">
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <link rel="stylesheet" href="css/style.css">
</head>

<body>'''

def extract_content_from_minified(html):
    """Extract body content from minified HTML"""
    # Find <body> content
    body_match = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    if body_match:
        return body_match.group(1)
    return None

def extract_title_from_html(html):
    """Extract title from HTML"""
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        return title_match.group(1)
    return "Blog Post"

def clean_blog_file(file_path):
    """Clean and standardize a blog file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = Path(file_path).name
    
    # Extract title
    title = extract_title_from_html(content)
    
    # Check if already has proper head
    if '<head>' in content and '<meta name="viewport"' in content and 'font-awesome' in content:
        # Already has proper structure
        return False, "Already standardized"
    
    # Extract body content
    body_content = extract_content_from_minified(content)
    
    if not body_content:
        # Try to find blog structure markers
        if '<article class="post-single">' in content or '<section class="blog">' in content:
            # Extract from section start
            blog_match = re.search(r'(<section class="blog">.*?</body>)', content, re.DOTALL)
            if blog_match:
                body_content = blog_match.group(1)
        else:
            return False, "No blog content found"
    
    if not body_content:
        return False, "Could not extract body content"
    
    # Create proper head
    proper_head = PROPER_HEAD_TEMPLATE.replace('{TITLE}', title).replace('{FILENAME}', filename)
    
    # Format body content - add basic formatting
    body_content = body_content.replace('><', '>\n<')
    
    # Combine
    new_html = proper_head + '\n  ' + body_content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True, "Standardized"

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    blog_files = sorted(base_dir.glob('blog-*.html'))
    
    print("🧹 Cleaning and standardizing blog files...\n")
    
    cleaned_count = 0
    
    for file in blog_files:
        try:
            was_cleaned, msg = clean_blog_file(str(file))
            if was_cleaned:
                print(f"✅ CLEANED: {file.name} - {msg}")
                cleaned_count += 1
            else:
                print(f"  OK: {file.name} - {msg}")
        except Exception as e:
            print(f"❌ ERROR: {file.name} - {str(e)}")
    
    print(f"\n{'='*70}")
    print(f"✅ Cleaned: {cleaned_count} files")
    print(f"📁 Total: {len(blog_files)} files")

if __name__ == '__main__':
    main()
